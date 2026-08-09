from flask import Flask

from app.config import Config
from app.extensions import db, migrate, jwt, cors, bcrypt
from app.models import Role, User
from app.auth import auth_bp
from app.animals import animals_bp
from app.rescues import rescues_bp
from app.adoptions import adoptions_bp
from app.ngos import ngos_bp
from app.volunteers import volunteers_bp

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
    app.register_blueprint(rescues_bp)
    app.register_blueprint(adoptions_bp)
    app.register_blueprint(ngos_bp)
    app.register_blueprint(volunteers_bp)

    @app.route("/")
    def home():
        return {
            "project": "AnimalCare",
            "version": "2.0",
            "status": "Backend Running Successfully"
        }

    return app