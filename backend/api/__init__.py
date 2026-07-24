from .auth import auth_bp
from .lobbies import lobbies_bp
from .games import games_bp

def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(lobbies_bp)
    app.register_blueprint(games_bp)