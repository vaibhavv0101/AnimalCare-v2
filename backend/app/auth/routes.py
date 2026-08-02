from flask import request, jsonify

from app.auth import auth_bp
from app.auth.schemas import RegisterSchema, LoginSchema
from app.auth.service import register_user, login_user

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