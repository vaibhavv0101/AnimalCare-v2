from functools import wraps

from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity

from app.models.user import User


def role_required(*allowed_roles):
    """
    Restrict an endpoint to specific user roles.

    Example:
        @role_required("Admin")
    """

    def decorator(function):

        @wraps(function)
        def wrapper(*args, **kwargs):

            # Verify JWT token
            verify_jwt_in_request()

            # Get logged-in user's ID
            user_id = get_jwt_identity()

            try:
                user_id = int(user_id)
            except (TypeError, ValueError):
                return jsonify({
                    "success": False,
                    "message": "Invalid user identity"
                }), 401

            # Find user
            user = User.query.get(user_id)

            if user is None:
                return jsonify({
                    "success": False,
                    "message": "User not found"
                }), 404

            # Check whether role exists
            if user.role is None:
                return jsonify({
                    "success": False,
                    "message": "User role not assigned"
                }), 403

            # Check allowed role
            if user.role.name not in allowed_roles:
                return jsonify({
                    "success": False,
                    "message": "Admin access required"
                }), 403

            return function(*args, **kwargs)

        return wrapper

    return decorator