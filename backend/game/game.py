import datetime
from backend.engine.board import Board
from backend.models.enums import PlayerColor, GameStatus, GameResult
from backend.models.time_control import TimeControl
from backend.models.move import Move

class Game:
    def __init__(self, game_id: int, white_player_id: int, red_player_id: int):
        self.game_id = game_id
        self.white_player_id = white_player_id
        self.red_player_id = red_player_id

        self.board = Board()
        self.current_turn = PlayerColor.WHITE
        self.status: GameStatus
        self.result: GameResult | None
        self.draw_offered_by: int | None # player_id

        # pieces on player's hand   piece_id, quantity
        self.white_pieces: dict[str, int]
        self.red_pieces: dict[str, int]

        self.time_control: TimeControl
        self.white_time_left: float
        self.red_time_left: float
        self.last_move_at: datetime

        self.moves: list[Move]
        self.started_at: datetime

        self.disconnected: dict # { player_id: disconnect_timer }

    def apply_move(self, move) -> MoveResult:
        pass

    def resign(self, player_id) -> GameResult:
        pass

    def propose_draw(self, player_id):
        pass

    def accept_draw(self, player_id) -> GameResult:
        pass

    def reject_draw(self, player_id):
        pass

    def on_player_disconnect(self, player_id):   # starts 60s timer
        pass

    def on_player_reconnect(self, player_id):    # canlcels timer
        pass

    def on_reconnect_timeout(self, player_id):
        pass

    def get_moves_string(self) -> str:
        pass

    def get_state_for_player(self, player_id) -> dict:
        pass
