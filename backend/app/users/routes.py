from flask import request, jsonify
from flask import jsonify
from flask_jwt_extended import jwt_required

from app.users import users_bp
from app.models.user import User


@users_bp.route("/", methods=["GET"])
@jwt_required()
def get_users():

    users = User.query.order_by(
        User.id.asc()
    ).all()

    result = []

    for user in users:

        result.append({
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "phone": user.phone,
            "is_verified": user.is_verified,
            "is_active": user.is_active,
            "role": user.role.name if user.role else None,
            "role_id": user.role_id,
            "created_at": (
                user.created_at.isoformat()
                if user.created_at
                else None
            )
        })

    return jsonify({
        "success": True,
        "count": len(result),
        "users": result
    }), 200


@users_bp.route("/<int:user_id>", methods=["GET"])
@jwt_required()
def get_user(user_id):

    user = User.query.get(user_id)

    if not user:
        return jsonify({
            "success": False,
            "message": "User not found"
        }), 404

    return jsonify({
        "success": True,
        "user": {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "phone": user.phone,
            "is_verified": user.is_verified,
            "is_active": user.is_active,
            "role": user.role.name if user.role else None,
            "role_id": user.role_id,
            "created_at": (
                user.created_at.isoformat()
                if user.created_at
                else None
            )
        }
    }), 200


@users_bp.route("/<int:user_id>/status", methods=["PUT"])
@jwt_required()
def update_user_status(user_id):

    from flask import request

    user = User.query.get(user_id)

    if not user:
        return jsonify({
            "success": False,
            "message": "User not found"
        }), 404

    data = request.get_json(silent=True) or {}

    if "is_active" not in data:
        return jsonify({
            "success": False,
            "message": "is_active is required"
        }), 400

    user.is_active = bool(data["is_active"])

    from app.extensions import db

    db.session.commit()

    return jsonify({
        "success": True,
        "message": "User status updated successfully",
        "user": {
            "id": user.id,
            "is_active": user.is_active
        }
    }), 200

@users_bp.route("/<int:user_id>/role", methods=["PUT"])
@jwt_required()
def update_user_role(user_id):

    user = User.query.get(user_id)

    if not user:
        return jsonify({
            "success": False,
            "message": "User not found"
        }), 404

    data = request.get_json(silent=True) or {}

    if "role_id" not in data:
        return jsonify({
            "success": False,
            "message": "role_id is required"
        }), 400

    from app.models.role import Role
    from app.extensions import db

    role = Role.query.get(data["role_id"])

    if not role:
        return jsonify({
            "success": False,
            "message": "Role not found"
        }), 404

    user.role_id = role.id

    db.session.commit()

    return jsonify({
        "success": True,
        "message": "User role updated successfully",
        "user": {
            "id": user.id,
            "role_id": user.role_id,
            "role": role.name
        }
    }), 200
    

@users_bp.route("/<int:user_id>/verification", methods=["PUT"])
@jwt_required()
def update_user_verification(user_id):

    user = User.query.get(user_id)

    if not user:
        return jsonify({
            "success": False,
            "message": "User not found"
        }), 404

    data = request.get_json(silent=True) or {}
    
    if "is_verified" not in data:
        return jsonify({
            "success": False,
            "message": "is_verified is required"
        }), 400

    user.is_verified = bool(data["is_verified"])

    from app.extensions import db
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "User verification status updated successfully",
        "user": {
            "id": user.id,
            "is_verified": user.is_verified
        }
    }), 200

@users_bp.route("/", methods=["POST"])
@jwt_required()
def create_user():

    data = request.get_json(silent=True) or {}

    required_fields = [
        "full_name",
        "email",
        "phone",
        "password",
        "role"
    ]

    for field in required_fields:
        if not data.get(field):
            return jsonify({
                "success": False,
                "message": f"{field} is required"
            }), 400

    existing_user = User.query.filter_by(
        email=data["email"]
    ).first()

    if existing_user:
        return jsonify({
            "success": False,
            "message": "Email already exists"
        }), 409

    from app.models.role import Role
    from app.extensions import db, bcrypt

    role = Role.query.filter_by(
        name=data["role"]
    ).first()

    if not role:
        return jsonify({
            "success": False,
            "message": "Role not found"
        }), 404

    hashed_password = bcrypt.generate_password_hash(
        data["password"]
    ).decode("utf-8")

    user = User(
        full_name=data["full_name"],
        email=data["email"],
        phone=data["phone"],
        password=hashed_password,
        role_id=role.id
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "User created successfully",
        "user": {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "role": role.name
        }
    }), 201
    