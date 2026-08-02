from flask_jwt_extended import get_jwt_identity

from app.extensions import db
from app.models.animal import Animal
from app.models.rescue import Rescue


def create_rescue(data):

    animal = Animal.query.get(data["animal_id"])

    if animal is None:
        return None

    rescue = Rescue(
        animal_id=data["animal_id"],
        reported_by=int(get_jwt_identity()),
        latitude=data["latitude"],
        longitude=data["longitude"],
        address=data["address"],
        priority=data["priority"],
        notes=data.get("notes")
    )

    db.session.add(rescue)
    db.session.commit()

    return rescue
def get_all_rescues():
    return Rescue.query.order_by(Rescue.created_at.desc()).all()

def get_rescue_by_id(rescue_id):
    return Rescue.query.get(rescue_id)

def update_rescue_status(rescue_id, data):

    rescue = Rescue.query.get(rescue_id)

    if rescue is None:
        return None

    rescue.status = data["status"]

    db.session.commit()

    return rescue