from flask import Blueprint

games_bp = Blueprint("games", __name__, url_prefix="/games")

@games_bp.route("/<int:game_id>", methods=["GET"])
def get_game(game_id):
    pass