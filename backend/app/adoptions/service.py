from flask_jwt_extended import get_jwt_identity

from app.extensions import db
from app.models.adoption import Adoption
from app.models.animal import Animal
from app.models.notification import Notification


# ============================================================
# CREATE ADOPTION APPLICATION
# ============================================================

def create_adoption(data):

    adoption = Adoption(
        animal_id=data["animal_id"],
        user_id=int(get_jwt_identity()),
        reason=data["reason"],
        phone=data["phone"],
        address=data["address"],
        occupation=data["occupation"]
    )

    db.session.add(adoption)
    db.session.commit()

    return adoption


# ============================================================
# GET MY ADOPTIONS
# ============================================================

def get_my_adoptions():

    user_id = int(get_jwt_identity())

    return Adoption.query.filter_by(
        user_id=user_id
    ).order_by(
        Adoption.created_at.desc()
    ).all()


# ============================================================
# GET ALL ADOPTIONS
# ============================================================

def get_all_adoptions():

    return Adoption.query.order_by(
        Adoption.created_at.desc()
    ).all()


# ============================================================
# GET ADOPTION BY ID
# ============================================================

def get_adoption_by_id(adoption_id):

    return Adoption.query.get(adoption_id)


# ============================================================
# APPROVE ADOPTION
# CREATE NOTIFICATION FOR USER
# ============================================================

def approve_adoption(adoption_id):

    adoption = Adoption.query.get(adoption_id)

    if adoption is None:
        return None

    animal = Animal.query.get(adoption.animal_id)

    if animal is None:
        return False

    adoption.status = "Approved"
    animal.adoption_status = "Adopted"

    notification = Notification(
        user_id=adoption.user_id,
        title="Adoption Approved",
        message=(
            f"Your adoption application for "
            f"{animal.name} has been approved."
        )
    )

    db.session.add(notification)
    db.session.commit()

    return adoption


# ============================================================
# REJECT ADOPTION
# CREATE NOTIFICATION FOR USER
# ============================================================

def reject_adoption(adoption_id):

    adoption = Adoption.query.get(adoption_id)

    if adoption is None:
        return None

    animal = Animal.query.get(adoption.animal_id)

    if animal is None:
        return False

    adoption.status = "Rejected"
    animal.adoption_status = "Available"

    notification = Notification(
        user_id=adoption.user_id,
        title="Adoption Application Update",
        message=(
            f"Your adoption application for "
            f"{animal.name} was not approved."
        )
    )

    db.session.add(notification)
    db.session.commit()

    return adoption


# ============================================================
# DELETE ADOPTION
# ============================================================

def delete_adoption(adoption_id):

    adoption = Adoption.query.get(adoption_id)

    if adoption is None:
        return False

    db.session.delete(adoption)
    db.session.commit()

    return True