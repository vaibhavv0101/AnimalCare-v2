from flask import Flask

from app.config import Config
from app.extensions import db, migrate, jwt, cors, bcrypt
from app.models import Role, User
from app.auth import auth_bp
from app.animals import animals_bp

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app)
    bcrypt.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(animals_bp)

    @app.route("/")
    def home():
        return {
            "project": "AnimalCare",
            "version": "2.0",
            "status": "Backend Running Successfully"
        }

    return app