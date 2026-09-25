"""
============================================================
AnimalCare - Stray Animal Rescue & Adoption Platform
============================================================

RECONSTRUCTED FILE
------------------
This app.py has been RECONSTRUCTED from the available
saved project resources.

IMPORTANT:
This is NOT the original deleted app.py.
The original source file could not be recovered exactly.

Recovered project characteristics:
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-JWT-Extended
- Flask-CORS
- Modular Blueprints
- AnimalCare Backend
- Animal / Rescue / Adoption / Auth / NGO / Volunteer modules

============================================================
"""
import os
from flask import Flask, jsonify

from app.config import Config
from app.extensions import db, migrate, jwt, cors


def create_app():
    """
    Create and configure the Flask application.
    """

    # --------------------------------------------------------
    # 1. Create Flask application
    # --------------------------------------------------------
    app = Flask(__name__)

    # --------------------------------------------------------
    # 2. Load configuration
    # --------------------------------------------------------
    app.config.from_object(Config)

    # --------------------------------------------------------
    # 3. Initialize Flask extensions
    # --------------------------------------------------------
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app)

    # --------------------------------------------------------
    # 4. Import models
    #
    # IMPORTANT:
    # Your current app/models/__init__.py contains User,
    # not UserS. Therefore User is used here.
    # --------------------------------------------------------
    try:
        from app.models import (
    Role,
    User,
    Animal,
    Adoption,
    NGO,
    Rescue,
    Volunteer,
    Notification,
)

        # Keep model imports active so SQLAlchemy can discover
        # the models when migrations are generated.
        _ = (
            Role,
            User,
            Animal,
            Adoption,
            NGO,
            Rescue,
            Volunteer,
        )

    except ImportError as e:
        print("WARNING: Model import problem:", e)

    # --------------------------------------------------------
    # 5. Register Authentication Blueprint
    # --------------------------------------------------------
    try:
        from app.auth import auth_bp

        app.register_blueprint(
            auth_bp,
            url_prefix="/api/auth"
        )

        print("✓ Auth blueprint registered")

    except ImportError as e:
        print("WARNING: Auth blueprint not registered:", e)

    # --------------------------------------------------------
    # 6. Register Animals Blueprint
    # --------------------------------------------------------
    try:
        from app.animals import animals_bp

        app.register_blueprint(
            animals_bp,
            url_prefix="/api/animals"
        )

        print("✓ Animals blueprint registered")

    except ImportError as e:
        print("WARNING: Animals blueprint not registered:", e)

    # --------------------------------------------------------
    # 7. Register Rescues Blueprint
    # --------------------------------------------------------
    try:
        from app.rescues import rescues_bp

        app.register_blueprint(
            rescues_bp,
            url_prefix="/api/rescues"
        )

        print("✓ Rescues blueprint registered")

    except ImportError as e:
        print("WARNING: Rescues blueprint not registered:", e)

    # --------------------------------------------------------
    # 8. Register Adoptions Blueprint
    # --------------------------------------------------------
    try:
        from app.adoptions import adoptions_bp

        app.register_blueprint(
            adoptions_bp,
            url_prefix="/api/adoptions"
        )

        print("✓ Adoptions blueprint registered")

    except ImportError as e:
        print("WARNING: Adoptions blueprint not registered:", e)

    # --------------------------------------------------------
    # 9. Register NGOs Blueprint
    # --------------------------------------------------------
    try:
        from app.ngos import ngos_bp

        app.register_blueprint(
            ngos_bp,
            url_prefix="/api/ngos"
        )

        print("✓ NGOs blueprint registered")

    except ImportError as e:
        print("WARNING: NGOs blueprint not registered:", e)

    # --------------------------------------------------------
    # 10. Register Volunteers Blueprint
    # --------------------------------------------------------
    try:
        from app.volunteers import volunteers_bp

        app.register_blueprint(
            volunteers_bp,
            url_prefix="/api/volunteers"
        )

        print("✓ Volunteers blueprint registered")

    except ImportError as e:
        print("WARNING: Volunteers blueprint not registered:", e)
    # --------------------------------------------------------
    # 11. Register Users Blueprint
    # --------------------------------------------------------
    try:
        from app.users import users_bp

        app.register_blueprint(
            users_bp,
            url_prefix="/api/users"
        )

        print("✓ Users blueprint registered")

    except ImportError as e:
        print("WARNING: Users blueprint not registered:", e)
            # ---------------------------------------------------------
    # 12. Register Notifications Blueprint
    # ---------------------------------------------------------

    try:
        from app.notifications import notifications_bp

        app.register_blueprint(notifications_bp)

        print("✓ Notifications blueprint registered")

    except ImportError as e:
        print("WARNING: Notifications blueprint not registered:", e)
    # --------------------------------------------------------
    # 11. Home route
    # --------------------------------------------------------
    @app.route("/")
    def home():
        return jsonify({
            "project": "AnimalCare",
            "version": "2.0",
            "status": "Backend Running Successfully"
        })

    # --------------------------------------------------------
    # 12. Health check route
    # --------------------------------------------------------
    @app.route("/api/health")
    def health_check():
        return jsonify({
            "success": True,
            "message": "AnimalCare API is running",
            "status": "healthy"
        })

    # --------------------------------------------------------
    # 13. 404 Error Handler
    # --------------------------------------------------------
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "message": "API endpoint not found"
        }), 404

    # --------------------------------------------------------
    # 14. 500 Error Handler
    # --------------------------------------------------------
    @app.errorhandler(500)
    def internal_error(error):

        try:
            db.session.rollback()
        except Exception:
            pass

        return jsonify({
            "success": False,
            "message": "Internal server error"
        }), 500

    # --------------------------------------------------------
    # 15. Return application
    # --------------------------------------------------------
    return app


# ============================================================
# Create Flask application
# ============================================================

app = create_app()


# ============================================================
# Run application
# ============================================================

if __name__ == "__main__":

    print()
    print("=" * 60)
    print("AnimalCare Backend")
    print("=" * 60)
    print("Server: http://127.0.0.1:5000")
    print("Health: http://127.0.0.1:5000/api/health")
    print("=" * 60)
    print()

    app.run(
    host="0.0.0.0",
    port=int(os.environ.get("PORT", 5000)),
    debug=False
)