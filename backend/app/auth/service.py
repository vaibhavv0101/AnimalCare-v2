from flask_jwt_extended import create_access_token

from app.extensions import db, bcrypt
from app.models.user import User
from app.models.role import Role


def register_user(data):

    existing = User.query.filter_by(email=data["email"]).first()

    if existing:
        return {"success": False, "message": "Email already exists"}, 409

    role = Role.query.filter_by(name=data["role"]).first()

    if not role:
        return {"success": False, "message": "Role not found"}, 404

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

    return {
        "success": True,
        "message": "User registered successfully"
    }, 201


def login_user(data):

    user = User.query.filter_by(email=data["email"]).first()

    if not user:
        return {
            "success": False,
            "message": "Invalid email or password"
        }, 401

    if not bcrypt.check_password_hash(
        user.password,
        data["password"]
    ):
        return {
            "success": False,
            "message": "Invalid email or password"
        }, 401

    token = create_access_token(identity=str(user.id))

    return {
        "success": True,
        "access_token": token,
        "user": {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "role": user.role.name
        }
    }, 200