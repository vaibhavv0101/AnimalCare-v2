from flask_jwt_extended import get_jwt_identity

from app.extensions import db
from app.models.adoption import Adoption
from app.models.animal import Animal

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

def get_all_adoptions():

    return Adoption.query.order_by(
        Adoption.created_at.desc()
    ).all()
    
def get_adoption_by_id(adoption_id):

    return Adoption.query.get(adoption_id)

def approve_adoption(adoption_id):

    adoption = Adoption.query.get(adoption_id)

    if adoption is None:
        return None

    animal = Animal.query.get(adoption.animal_id)

    if animal is None:
        return False

    adoption.status = "Approved"
    animal.adoption_status = "Adopted"

    db.session.commit()

    return adoption

def reject_adoption(adoption_id):

    adoption = Adoption.query.get(adoption_id)

    if adoption is None:
        return None

    adoption.status = "Rejected"

    db.session.commit()

    return adoption

def delete_adoption(adoption_id):

    adoption = Adoption.query.get(adoption_id)

    if adoption is None:
        return False

    db.session.delete(adoption)
    db.session.commit()

    return True