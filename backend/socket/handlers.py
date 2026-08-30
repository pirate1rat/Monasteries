from flask import request, session
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_login import current_user

from backend.manager_instance import game_manager
from backend.models.move import Move
from backend.models.placement import Placement
from backend.models.enums import PlayerColor, GameStatus


_lobby_host_sids: dict[str, str] = {}

OPPOSITE: dict[PlayerColor, PlayerColor] = {
    PlayerColor.WHITE: PlayerColor.RED,
    PlayerColor.RED: PlayerColor.WHITE,
}

def get_current_player_id():
    return current_user.user_id if current_user.is_authenticated else session.get("player_id")

def register_handlers(socketio: SocketIO):

    #connection
    @socketio.on("connect")
    def handle_connect():
        player_id = get_current_player_id()
        if player_id is None:
            return

        game = game_manager.get_game_for_player(player_id)
        if game is None:
            return

        room = str(game.game_id)
        game_manager.handle_reconnect(game.game_id, player_id)
        emit("game_state", game.get_state_for_player(player_id))
        emit("opponent reconnected", {}, room=room, include_self=False)

    @socketio.on("disconnect")
    def handle_disconnect(reason):
        player_id = get_current_player_id()
        if player_id is None:
            return

        game = game_manager.get_game_for_player(player_id)
        if game is None:
            return

        room = str(game.game_id)

        def on_timeout(game_id, result):
            socketio.emit("game_over", {"result": result.value}, room=room)
            game_manager.end_game(game_id)

        game_manager.handle_disconnect(game.game_id, player_id, on_timeout)
        emit("opponent_disconnected", {"reconnected_time_left": 60}, room=room, include_self=False)

    #lobby
    @socketio.on("watch_lobby")
    def handle_watch_lobby(data):
        lobby_id = data.get("lobby_id")
        if lobby_id:
            _lobby_host_sids[lobby_id] = request.sid

    @socketio.on("join_lobby")
    def handle_join_lobby(data):
        player_id = get_current_player_id()
        lobby_id = data.get("lobby_id")

        game = game_manager.join_lobby(lobby_id, player_id)
        if game is None:
            emit("error", {"code": "LOBBY_NOT_FOUND"})
            return

        room = str(game.game_id)
        join_room(room)

        host_sid = _lobby_host_sids.pop(lobby_id, None)
        if host_sid:
            emit("game_started", {
                "game_id": game.game_id,
                "board": game.board.to_serializable(),
                "white_player": game.players.inverse[PlayerColor.WHITE],
                "red_player": game.players.inverse[PlayerColor.RED],
                "time_control": {
                    "base": game.time_control.base,
                    "increment": game.time_control.incremental,
                },
                "current_turn": game.current_turn.value,
            }, to=host_sid)
        
        emit("game_started", {
            "game_id": game.game_id,
            "board": game.board.to_serializable(),
            "white_player": game.players.inverse[PlayerColor.WHITE],
            "red_player": game.players.inverse[PlayerColor.RED],
            "time_control": {
                "base": game.time_control.base,
                "increment": game.time_control.incremental,
            },
            "current_turn": game.current_turn.value,
        })

    @socketio.on("cancel_lobby")
    def handle_cancel_lobby(data):
        player_id = get_current_player_id()
        lobby_id  = data.get("lobby_id")

        success = game_manager.cancel_lobby(lobby_id, player_id)
        if not success:
            emit("error", {"code": "LOBBY_NOT_FOUND"})
            return

        _lobby_host_sids.pop(lobby_id, None)
        socketio.emit("lobby_cancelled", {"lobby_id": lobby_id})

    @socketio.on("join_game")
    def handle_join_game(data):
        player_id = get_current_player_id()
        game_id = int(data.get("game_id"))

        game = game_manager.get_game(game_id)
        if game is None:
            emit("error", {"code": "GAME_NOT_FOUND"})
            return

        if player_id not in game.players:
            emit("error", {"code": "NOT_A_PLAYER"})
            return

        join_room(str(game_id))
        emit("game_state", game.get_state_for_player(player_id))

    #game
    @socketio.on("make_move")
    def handle_make_move(data):
        player_id = get_current_player_id()
        game_id = int(data.get("game_id"))

        game = game_manager.get_game(game_id)
        if game is None:
            emit("error", {"code": "LOBBY_NOT_FOUND"})
            return

        placement = Placement(
            token_id = "",
            piece_id = data["piece_id"],
            anchor = tuple(data["anchor"]),
            rotation = data["rotation"],
            color = game._color(player_id) if data["piece_id"] != 0 else PlayerColor.NEUTRAL 
        )
        move = Move(placement, move_timestamp=0)
        result = game.apply_move(player_id, move)
        if result is None:
            emit("error", {"code": "INVALID_MOVE"})

        room = str(game_id)

        if game.status == GameStatus.FINISHED:
            emit("game_over", {
                "result": game.result.value,
                "final_board": game.board.to_serializable(),
                "white_time": game.white_time_left,
                "red_time": game.red_time_left,
            }, room=room)
            game_manager.end_game(game_id)
        else:
            emit("move_made", {
                "board": game.board.to_serializable(),
                "current_turn": game.current_turn.value,
                "white_pieces": {
                    str(pid): qty
                    for pid, qty in game.pieces_on_hand[PlayerColor.WHITE].items()
                },
                "red_pieces": {
                    str(pid): qty
                    for pid, qty in game.pieces_on_hand[PlayerColor.RED].items()
                },
                "white_time": game.white_time_left,
                "red_time": game.red_time_left,
                "token_id": result.token_id,
                "captured": result.captured.token_id if result.captured else None,
                "territories_gained": list(result.territories_gained),
                "opponent_auto_passed": result.opponent_auto_passed,
                "move_notation": game._format_move(game.moves[-1]),
                "move_player": OPPOSITE[game.current_turn].value, #who played move

        }, room=room)

    @socketio.on("resign")
    def handle_resign(data):
        player_id = get_current_player_id()
        game_id = int(data.get("game_id"))

        game = game_manager.get_game(game_id)
        if game is None:
            emit("error", {"code": "GAME_NOT_FOUND"})
            return

        room = str(game_id)
        result = game.resign(player_id)
        emit("game_over", {"result": result.value}, room=room)
        game_manager.end_game(game_id)

    @socketio.on("propose_draw")
    def handle_propose_draw(data):
        player_id = get_current_player_id()
        game_id = int(data.get("game_id"))

        game = game_manager.get_game(game_id)
        if game is None:
            emit("error", {"code": "GAME_NOT_FOUND"})
            return

        if not game.propose_draw(player_id):
            emit("error", {"code": "DRAW_ALREADY_OFFERED"})
            return

        room = str(game_id)
        emit("draw_proposed", {"by": game._color(player_id).value}, room=room)

    @socketio.on("accept_draw")
    def handle_accept_draw(data):
        player_id = get_current_player_id()
        game_id = int(data.get("game_id"))

        game = game_manager.get_game(game_id)
        if game is None:
            emit("error", {"code": "GAME_NOT_FOUND"})
            return

        result = game.accept_draw(player_id)
        if result is None:
            emit("error", {"code": "INVALID_DRAW_ACCEPT"})
            return

        room = str(game_id)
        emit("game_over", {"result": result.value}, room=room)
        game_manager.end_game(game_id)

    @socketio.on("reject_draw")
    def handle_reject_draw(data):
        player_id = get_current_player_id()
        game_id = int(data.get("game_id"))

        game = game_manager.get_game(game_id)
        if game is None:
            emit("error", {"code": "GAME_NOT_FOUND"})
            return

        result = game.reject_draw(player_id)
        if not result:
            emit("error", {"code": "INVALID_DRAW_REJECTION"})
            return

        room = str(game_id)
        emit("draw_rejected", {}, room=room)