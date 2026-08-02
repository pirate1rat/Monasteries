from flask import Blueprint, jsonify, request, session
from flask_login import current_user, login_required

from backend.models.time_control import TimeControl
from backend.manager_instance import game_manager
from backend.db.operations import get_user_by_id
lobbies_bp = Blueprint("lobbies", __name__, url_prefix="/lobbies")


@lobbies_bp.route("/", methods=["GET", "POST"])
def get_or_create_lobbies():
    def lobby_to_dict(lobby):
        if current_user.is_authenticated:
            host_id = current_user.user_id
            host_name = get_user_by_id(lobby.host_id).username
        else:
            host_id = session.get('player_id')
            host_name = "Guest"

        return {
        "lobby_id": str(lobby.lobby_id),
        "host_id": host_id,
        "host_name": host_name,
        "host_color": lobby.host_color,
        "time_control": {
            "base": lobby.time_control.base,
            "incremental": lobby.time_control.incremental,
        },
        "created_at": lobby.created_at.isoformat(),
    }

    if request.method == 'GET':
        return jsonify({"status": "ok", 
                        "lobbies": [lobby_to_dict(l) for l in game_manager.active_lobbies.values()]})
    else:
        data = request.get_json()
        if current_user.is_authenticated:
            host_id = current_user.user_id
        else:
            host_id = session.get('player_id')
    
        game_manager.create_lobby(host_id, data["color"], TimeControl(**data["timeControl"]))
        return jsonify({"status": "ok"})

# @lobbies_bp.route("/", methods=["POST"])
# @login_required
# def create_lobby():
#     pass
