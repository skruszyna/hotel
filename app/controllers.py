from flask import Blueprint, request, jsonify
from app.models import db, User

bp = Blueprint("main", __name__)

@bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided"}), 400

    email = data.get("email")
    password = data.get("password")

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists"}), 400

    user = User(
        first_name=data.get("first_name"),
        last_name=data.get("last_name"),
        email=email,
        phone=data.get("phone")
    )
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201
