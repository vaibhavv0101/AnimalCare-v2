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