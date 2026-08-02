from flask import request, jsonify

from app.auth import auth_bp
from app.auth.schemas import RegisterSchema, LoginSchema
from app.auth.service import register_user, login_user
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User

register_schema = RegisterSchema()
login_schema = LoginSchema()


@auth_bp.route("/health", methods=["GET"])
def health():
    return jsonify({
        "success": True,
        "message": "Authentication module is working"
    })


@auth_bp.route("/register", methods=["POST"])
def register():

    errors = register_schema.validate(request.json)

    if errors:
        return jsonify(errors), 400

    response, status = register_user(request.json)

    return jsonify(response), status


@auth_bp.route("/login", methods=["POST"])
def login():

    errors = login_schema.validate(request.json)

    if errors:
        return jsonify(errors), 400

    response, status = login_user(request.json)

    return jsonify(response), status

@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():

    user_id = get_jwt_identity()

    user = User.query.get(user_id)

    return {
        "success": True,
        "user": {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "role": user.role.name
        }
    }