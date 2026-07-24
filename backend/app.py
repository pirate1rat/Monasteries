from flask import Flask, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_socketio import SocketIO

from backend.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
socketio = SocketIO()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    app.config.from_object("backend.config.Config")

    CORS(app, origins="http://localhost:3000")

    db.init_app(app)
    bcrypt.init_app(app)
    socketio.init_app(app, cors_allowed_origins="http://localhost:3000")
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id: str):
        from backend.db.user import User
        return db.session.get(User, int(user_id))
    
    @login_manager.unauthorized_handler
    def unauthorized_callback():
        return jsonify({"error": "unauthorized"}), 401

    Migrate(app, db)

    from backend.api import register_blueprints
    from backend.socket.handlers import register_handlers

    register_blueprints(app)
    register_handlers(socketio)

    return app