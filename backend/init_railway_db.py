from app import create_app
from app.extensions import db, bcrypt
from app.models import (
    Role,
    User,
    Animal,
    Rescue,
    Adoption,
    NGO,
    Volunteer,
    Notification,
)

app = create_app()

with app.app_context():

    print("Creating AnimalCare database tables...")

    db.create_all()

    print("Tables created successfully.")

    # --------------------------------------------------
    # Create required roles
    # --------------------------------------------------

    role_names = [
        "Admin",
        "User",
        "NGO",
        "Volunteer",
    ]

    for role_name in role_names:

        role = Role.query.filter_by(
            name=role_name
        ).first()

        if not role:
            role = Role(name=role_name)
            db.session.add(role)
            print(f"Created role: {role_name}")
        else:
            print(f"Role already exists: {role_name}")

    db.session.commit()

    print("Roles initialized successfully.")

    # --------------------------------------------------
    # Verify tables
    # --------------------------------------------------

    print("\nAnimalCare Railway database initialized.")
    print("Do NOT create the Admin password in this script yet.")