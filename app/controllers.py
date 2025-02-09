from flask import Blueprint, request, jsonify
from app.models import db, User, Service

bp = Blueprint("main", __name__)

# ========================================
#  REJESTRACJA UŻYTKOWNIKA
# ========================================
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

# ========================================
#  WYŚWIETLANIE DOSTĘPNYCH USŁUG
# ========================================
@bp.route("/api/services", methods=["GET"])
def get_services():
    """Zwraca listę dostępnych usług posortowanych według kategorii."""
    category = request.args.get("category")
    
    if category:
        services = Service.query.filter_by(category=category).all()
    else:
        services = Service.query.order_by(Service.category).all()

    result = [{
        "id": service.id,
        "name": service.name,
        "description": service.description,
        "price": service.price,
        "duration": service.duration,
        "category": service.category,
        "availability": service.availability
    } for service in services]

    return jsonify(result), 200

# ========================================
#  DODAWANIE NOWEJ USŁUGI
# ========================================
@bp.route("/api/services", methods=["POST"])
def add_service():
    """Dodaje nową usługę do systemu."""
    data = request.get_json()

    required_fields = ["name", "description", "price", "duration", "category", "availability"]
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({"error": f"Field '{field}' is required"}), 400

    new_service = Service(
        name=data["name"],
        description=data["description"],
        price=float(data["price"]),
        duration=data["duration"],
        category=data["category"],
        availability=data["availability"]
    )

    db.session.add(new_service)
    db.session.commit()

    return jsonify({"message": "Service added successfully", "service_id": new_service.id}), 201
