from app.extensions import db
from app.models.ngo import NGO


def create_ngo(data):

    ngo = NGO(
        name=data["name"],
        email=data["email"],
        phone=data["phone"],
        address=data["address"],
        registration_number=data.get("registration_number"),
        description=data.get("description")
    )

    db.session.add(ngo)
    db.session.commit()

    return ngo


def get_all_ngos():

    return NGO.query.order_by(
        NGO.created_at.desc()
    ).all()
    
def get_ngo_by_id(ngo_id):

    return NGO.query.get(ngo_id)

def update_ngo(ngo_id, data):

    ngo = NGO.query.get(ngo_id)

    if ngo is None:
        return None

    if "name" in data:
        ngo.name = data["name"]

    if "email" in data:
        ngo.email = data["email"]

    if "phone" in data:
        ngo.phone = data["phone"]

    if "address" in data:
        ngo.address = data["address"]

    if "registration_number" in data:
        ngo.registration_number = data["registration_number"]

    if "description" in data:
        ngo.description = data["description"]

    if "status" in data:
        ngo.status = data["status"]

    db.session.commit()

    return ngo

def delete_ngo(ngo_id):

    ngo = NGO.query.get(ngo_id)

    if ngo is None:
        return False

    db.session.delete(ngo)
    db.session.commit()

    return True