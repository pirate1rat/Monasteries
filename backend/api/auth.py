import os

from flask import Blueprint, session, request, jsonify
from flask_login import login_user, logout_user, current_user

from backend.app import bcrypt
from backend.db.operations import create_user, username_exists, email_exists, get_user_by_email

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=['POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        user = get_user_by_email(data["email"])

        if user is None or not bcrypt.check_password_hash(user.password, data["password"]):
            return jsonify({"error": "invalid credentials"}), 401

        session.permanent = True
        login_user(user, remember=True)
        return jsonify({"status": "ok"})

@auth_bp.route("/logout", methods=['POST'])
def logout():
    logout_user()
    return jsonify({"status": "ok"})

@auth_bp.route("/register", methods=['POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        hashed_password = bcrypt.generate_password_hash(data["password"])
        if not (username_exists(data["username"]) or email_exists(data["email"])): 
            create_user(data["username"], data["email"], hashed_password)
            return jsonify({"status": "ok"})
        else:
            return jsonify({"error": "username or email already taken"}), 409

@auth_bp.route("/me", methods=['GET'])
def me():
    if current_user.is_authenticated:
        return jsonify({
            "status": "ok",
            "player_id": current_user.user_id,
            "username":  current_user.username,
            "anonymous": False,
        })

    player_id = session.get("player_id")
    if player_id:
        return jsonify({
            "status": "ok",
            "player_id": player_id,
            "username":  None,
            "anonymous": True,
        })
    else:
        anon_id = -abs(hash(os.urandom(8)))
        session["player_id"] = anon_id
        session["is_anonymous"] = True
        session.permanent = True
        return jsonify({
            "status": "ok", 
            "player_id": anon_id, 
            "username":  None,
            "anonymous": True,
        })

#to delete in future
@auth_bp.route("/anonymous", methods=['POST'])
def anonymous():
    anon_id = -abs(hash(os.urandom(8)))
    session["player_id"] = anon_id
    session["is_anonymous"] = True
    session.permanent = True
    return jsonify({"status": "ok", "player_id": anon_id})