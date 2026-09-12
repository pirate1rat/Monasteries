import os

from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from flask_migrate import Migrate
from backend.instances import db, bcrypt, login_manager, socketio

def create_app():
    app = Flask(
        __name__,
        static_folder=os.path.join(os.path.dirname(__file__), "../frontend/dist"),
        static_url_path="/static"
    )

    app.config.from_object("backend.config.Config")

    origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5000").split(",")
    CORS(app, origins=origins, supports_credentials=True)

    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def serve(path):
        static = app.static_folder
        full = os.path.join(static, path)
        print(f"SERVE CALLED: path={path}")
        if path and os.path.exists(full):
            return send_from_directory(static, path)
        return send_from_directory(static, "index.html")

    db.init_app(app)
    bcrypt.init_app(app)
    socketio.init_app(
        app, 
        cors_allowed_origins="*",
        logger=True,
        engineio_logger=True
    )
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