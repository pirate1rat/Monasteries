import os

from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from flask_migrate import Migrate

from backend.instances import db, bcrypt, login_manager, socketio

FRONTEND_DIST = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")
)

API_PREFIXES = ("auth", "lobbies", "games", "socket.io")

DEV_ORIGINS = ["http://localhost:5173", "http://127.0.0.1:5173"]


def resolve_origins(is_dev: bool):
    """ALLOWED_ORIGINS from .env wins; otherwise Vite in dev, anything on LAN."""
    raw = os.getenv("ALLOWED_ORIGINS", "")
    origins = [o.strip() for o in raw.split(",") if o.strip()]
    if origins:
        return origins
    return DEV_ORIGINS if is_dev else "*"


def create_app(mode: str = "prod"):
    if mode not in ("dev", "prod"):
        raise ValueError(f"unknown mode: {mode!r}")
    is_dev = mode == "dev"

    app = Flask(__name__, static_folder=None)
    app.config.from_object("backend.config.Config")
    app.config["DEBUG"] = is_dev

    if not is_dev and not os.getenv("SECRET_KEY"):
        app.logger.warning("SECRET_KEY is not set - using the insecure default. Set it in .env")

    origins = resolve_origins(is_dev)
    CORS(app, origins=origins, supports_credentials=True)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(
        app,
        async_mode="threading",
        cors_allowed_origins=origins,
        logger=True,
        engineio_logger=True,
    )
    Migrate(app, db)

    @login_manager.user_loader
    def load_user(user_id: str):
        from backend.db.user import User
        return db.session.get(User, int(user_id))

    @login_manager.unauthorized_handler
    def unauthorized_callback():
        return jsonify({"error": "unauthorized"}), 401

    from backend.api import register_blueprints
    from backend.socket.handlers import register_handlers

    register_blueprints(app)
    register_handlers(socketio)

    if not is_dev:
        @app.route("/", defaults={"path": ""})
        @app.route("/<path:path>")
        def serve_frontend(path):
            if path.split("/")[0] in API_PREFIXES:
                return jsonify({"error": "not found"}), 404
            full = os.path.join(FRONTEND_DIST, path)
            if path and os.path.isfile(full):
                return send_from_directory(FRONTEND_DIST, path)
            return send_from_directory(FRONTEND_DIST, "index.html")

    return app