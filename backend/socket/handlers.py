from flask import request, session
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_login import current_user

from backend.manager_instance import game_manager
from backend.models.move import Move
from backend.models.placement import Placement
from backend.models.enums import PlayerColor, GameStatus


def register_handlers(socketio: SocketIO):

    #connection
    @socketio.on("connect")
    def handle_connect():
        #TODO
        pass

    @socketio.on("disconnect")
    def handle_disconnect():
        #TODO
        pass

    #lobby
    @socketio.on("join_lobby")
    def handle_join_lobby(data):
        player_id = current_user.user_id if current_user.is_authenticated else session["player_id"]
        lobby_id = data.get("lobby_id")

        game = game_manager.join_lobby(lobby_id, player_id)
        if game is None:
            emit("error", {"code": "LOBBY_NOT_FOUND"})
            return

        room = str(game.game_id)
        join_room(room)

        emit("game_started", {
            "game_id": game.game_id,
            "board": game.board.to_serializable(),
            "white_player": game.players.inverse[PlayerColor.WHITE],
            "red_player": game.players.inverse[PlayerColor.RED],
            "time_control": {
                "base": game.time_control.base,
                "increment": game.time_control.increment,
            },
            "current_turn": game.current_turn.value,
        }, room=room)

    #game
    @socketio.on("make_move")
    def handle_make_move(data):
        player_id = current_user.user_id if current_user.is_authenticated else session["player_id"]
        game_id = data.get("game_id")

        game = game_manager.get_game(game_id)
        if game is None:
            emit("error", {"code": "LOBBY_NOT_FOUND"})
            return

        placement = Placement(
            token_id = "",
            piece_id = data["piece_id"],
            anchor = tuple(data["anchor"]),
            rotation = data["rotation"],
            color = game._color(player_id),
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
                "token_id": result.token_id,
                "captured": result.captured.token_id if result.captured else None,
                "territories_gained": list(result.territories_gained),
                "board": game.board.to_serializable(),
                "current_turn": game.current_turn.value,
                "white_time": game.white_time_left,
                "red_time": game.red_time_left,
                "opponent_auto_passed": result.opponent_auto_passed,
        }, room=room)

    @socketio.on("resign")
    def handle_resign(data):
        player_id = current_user.user_id if current_user.is_authenticated else session["player_id"]
        game_id = data.get("game_id")

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
        player_id = current_user.user_id if current_user.is_authenticated else session["player_id"]
        game_id = data.get("game_id")

        game = game_manager.get_game(game_id)
        if game is None:
            emit("error", {"code": "GAME_NOT_FOUND"})
            return

        if not game.propose_draw(player_id):
            emit("error", {"code": "DRAW_ALREADY_OFFERED"})
            return

        room = str(game_id)
        emit("draw_propossed", {"by": player_id}, room=room)

    @socketio.on("accept_draw")
    def handle_accept_draw(data):
        player_id = current_user.user_id if current_user.is_authenticated else session["player_id"]
        game_id = data.get("game_id")

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
        player_id = current_user.user_id if current_user.is_authenticated else session["player_id"]
        game_id = data.get("game_id")

        game = game_manager.get_game(game_id)
        if game is None:
            emit("error", {"code": "GAME_NOT_FOUND"})
            return

        result = game.reject_draw(player_id)
        if result is None:
            emit("error", {"code": "INVALID_DRAW_REJECTION"})
            return

        room = str(game_id)
        emit("draw_rejected", {}, room=room)