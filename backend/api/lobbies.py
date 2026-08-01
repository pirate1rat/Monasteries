from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required

from backend.manager_instance import game_manager
lobbies_bp = Blueprint("lobbies", __name__, url_prefix="/lobbies")


@lobbies_bp.route("/", methods=["GET"])
@login_required
def get_lobbies():
    pass

@lobbies_bp.route("/create", methods=["POST"])
@login_required
def create_lobby():
    if request.method == 'POST':
        data = request.get_json()
        game_manager.create_lobby(data["hostId"], data["color"], data["timeControl"])
        return jsonify({"status": "ok"})
