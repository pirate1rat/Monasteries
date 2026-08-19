import datetime
import threading
from bidict import bidict

from backend.engine.board import Board
from backend.engine.engine import Engine
from backend.models.piece import PIECE_CATALOG, PASS_TURN_ID
from backend.models.enums import PlayerColor, GameStatus, GameResult, PieceType
from backend.models.time_control import TimeControl
from backend.models.move import Move
from backend.models.move_result import MoveResult

from backend.db.operations import save_game

OPPOSITE: dict[PlayerColor, PlayerColor] = {
    PlayerColor.WHITE: PlayerColor.RED,
    PlayerColor.RED: PlayerColor.WHITE,
}

class Game:
    def __init__(
            self, 
            game_id: int, 
            white_player_id: int,
            red_player_id: int,
            time_control: TimeControl
        ):
        """ 
        Convention: all public methods accept `player_id: int`. The player's 
        color is resolved internally via `self._color(player_id)`. `Game` never 
        sends messages directly to clients—it only returns results. 
        The Socket.IO layer is responsible for delivering them to clients.
        """

        self.game_id = game_id

        # bidict[player_id -> PlayerColor]
        self.players = bidict({
            white_player_id: PlayerColor.WHITE,
            red_player_id: PlayerColor.RED
        })

        self.board = Board()
        self.current_turn = PlayerColor.WHITE #player color in current turn
        self.status = GameStatus.IN_PROGRESS
        self.result: GameResult | None = None
        self.draw_offered_by: int | None = None # player_id

        # pieces on player's hand   piece_id, quantity
        self.pieces_on_hand: dict[PlayerColor, dict[int, int]] = self._init_pieces()

        self.time_control = time_control
        self.white_time_left = float(time_control.base)
        self.red_time_left = float(time_control.base)
        now = datetime.datetime.now()
        self.started_at = now
        self.finished_at = None
        self.last_move_at = now

        self.moves: list[Move] = []
        self.history: list[dict] = []

        self.disconnected: dict[int, threading.Timer] = {} # { player_id: disconnect_timer }

    ###########################

    def _init_pieces(self) -> dict[PlayerColor, dict[int, int]]:
        res: dict[PlayerColor, dict[int, int]] = {
            PlayerColor.WHITE: {},
            PlayerColor.RED: {},
        }

        for piece_id, prefab in PIECE_CATALOG.items():
            if prefab.color != PlayerColor.NEUTRAL:
                res[prefab.color][piece_id] = prefab.starting_amount
        #giving cathedral to white player
        res[PlayerColor.WHITE][PieceType.CATHEDRAL.value] = PIECE_CATALOG[PieceType.CATHEDRAL.value].starting_amount

        return res

    def _color(self, player_id) -> PlayerColor:
        return self.players[player_id]

    def _player_id(self, color: PlayerColor) -> int:
        return self.players.inverse[color]
    
    def _time_left(self, color: PlayerColor) -> float:
        return self.white_time_left if color == PlayerColor.WHITE else self.red_time_left

    def _set_time_left(self, color: PlayerColor, value: float):
        if color == PlayerColor.WHITE:
            self.white_time_left = value
        else:
            self.red_time_left = value
    
    def _finish(self, result: GameResult):
        self.status = GameStatus.FINISHED
        self.result = result
        self.finished_at = datetime.datetime.now()

    def _tick_clock(self, color: PlayerColor):
        """
        Subtracts the time elapsed since the last move and adds the increment
        """

        now = datetime.datetime.now()
        elapsed = (now - self.last_move_at).total_seconds()
        self._set_time_left(color, self._time_left(color) - elapsed + self.time_control.incremental)
        self.last_move_at = now
    
    def _validate_turn(self, player_id: int) -> bool:
        return (self.status == GameStatus.IN_PROGRESS and self._color(player_id) == self.current_turn)

    def _advance_turn(self) -> GameResult | None:
        """
        Switches the turn. If the next player has no legal moves, their turn is 
        automatically passed, and the game-over condition is checked. 
        
        Returns: GameResult: if the game has ended. 
        None: if the game is still in progress.
        """
        self.current_turn = OPPOSITE[self.current_turn]

        if not Engine.has_possible_moves(
            self.board,
            self.current_turn,
            self.pieces_on_hand[self.current_turn],
        ):
            # autopass
            self.current_turn = OPPOSITE[self.current_turn]
            return Engine.check_game_over(
                self.board,
                self.pieces_on_hand[PlayerColor.WHITE],
                self.pieces_on_hand[PlayerColor.RED],
            )

        return None

    ##############################

    def apply_move(self, player_id: int,  move: Move) -> MoveResult | None:
        if not self._validate_turn(player_id): return None

        color = self._color(player_id)
        placement = move.placement

        # pass turn
        if placement.piece_id == PASS_TURN_ID:
            self._tick_clock(color)
            self.moves.append(move)
            self.history.append(self.board.to_serializable())

            game_result = self._advance_turn()
            if game_result is not None:
                self._finish(game_result)
            
            save_game(self)
            return MoveResult(token_id=PASS_TURN_ID, captured=None, territories_gained=set())

        result: MoveResult = self.board.place_piece(placement)
        if result is None:
            save_game(self)
            return None

        hand = self.pieces_on_hand.get(color, {})
        if placement.piece_id in hand:
            hand[placement.piece_id] -= 1
            if hand[placement.piece_id] == 0:
                del hand[placement.piece_id]
        
        self._tick_clock(color)
        self.moves.append(move)
        self.history.append(self.board.to_serializable())

        game_result = self._advance_turn()
        if game_result is not None:
            self._finish(game_result)
        else:
            result.opponent_auto_passed = not Engine.has_possible_moves(
                self.board,
                self.current_turn,
                self.pieces_on_hand[self.current_turn],
            )
        
        save_game(self)
        return result
            
    def resign(self, player_id) -> GameResult:
        color = self._color(player_id)
        result = GameResult.RED_WINS if color == PlayerColor.WHITE else GameResult.WHITE_WINS
        self._finish(result)
        return result 

    def propose_draw(self, player_id) -> bool:
        if self.draw_offered_by is not None:
            return False
        self.draw_offered_by = player_id
        return True

    def accept_draw(self, player_id) -> GameResult:
        if self.draw_offered_by is None or self.draw_offered_by == player_id:
            return None
        self.draw_offered_by = None
        self._finish(GameResult.DRAW)
        return GameResult.DRAW

    def reject_draw(self, player_id) -> bool:
        if self.draw_offered_by is None:
            return False
        self.draw_offered_by = None
        return True

    def on_player_disconnect(self, player_id, on_timeout):
        def _timeout():
            result = self.resign(player_id)
            self.status = GameStatus.ABANDONED
            on_timeout(self.game_id, result)
        
        timer = threading.Timer(60.0, _timeout)
        self.disconnected[player_id] = timer
        timer.start

    def on_player_reconnect(self, player_id):
        timer = self.disconnected.pop(player_id, None)
        if timer: timer.cancel()

    def on_reconnect_timeout(self, player_id) -> GameResult:
        if self.players[player_id] == PlayerColor.WHITE:
            return GameResult.RED_WINS
        else:
            return GameResult.WHITE_WINS

    def get_moves_string(self) -> str:
        parts = []
        for move in self.moves:
            p = move.placement
            if p.piece_id == PASS_TURN_ID:
                parts.append("_")
            else:
                col = chr(ord('A') + p.anchor[0])
                row = p.anchor[1] + 1
                parts.append(f"{col}{row}.{p.piece_id}.{p.rotation}.{move.move_timestamp}")
        return ";".join(parts)

    def get_state_for_player(self, player_id: int) -> dict:
        color = self._color(player_id)
        opp_color = OPPOSITE[color]
        return {
            "game_id":         self.game_id,
            "board":           self.board.to_serializable(),
            "player_color":    color.value,
            "current_turn":    self.current_turn.value,
            "player_pieces":   self.pieces_on_hand[color],
            "opponent_pieces": self.pieces_on_hand[opp_color],
            "player_time":     self._time_left(color),
            "opponent_time":   self._time_left(opp_color),
            "moves":           self.get_moves_string(),
            "status":          self.status.value,
            "result":          self.result.value if self.result else None,
            "draw_offered_by": self.draw_offered_by,
        }
