from flask import Blueprint, jsonify
from flask_login import current_user, login_required

lobbies_bp = Blueprint("lobbies", __name__, url_prefix="/lobbies")


@lobbies_bp.route("/", methods=["GET"])
@login_required
def get_lobbies():
    pass

@lobbies_bp.route("/", methods=["POST"])
@login_required
def create_lobby():
    pass