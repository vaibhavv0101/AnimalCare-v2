from app.extensions import db
from app.models.volunteer import Volunteer


def create_volunteer(data):

    volunteer = Volunteer(
        name=data["name"],
        email=data["email"],
        phone=data["phone"],
        address=data["address"],
        skills=data.get("skills"),
        availability=data.get(
            "availability",
            "Available"
        )
    )

    db.session.add(volunteer)
    db.session.commit()

    return volunteer

def get_all_volunteers():

    return Volunteer.query.order_by(
        Volunteer.created_at.desc()
    ).all()


def get_volunteer_by_id(volunteer_id):

    return Volunteer.query.get(volunteer_id)

def update_volunteer(volunteer_id, data):

    volunteer = Volunteer.query.get(volunteer_id)

    if volunteer is None:
        return None

    if "name" in data:
        volunteer.name = data["name"]

    if "email" in data:
        volunteer.email = data["email"]

    if "phone" in data:
        volunteer.phone = data["phone"]

    if "address" in data:
        volunteer.address = data["address"]

    if "skills" in data:
        volunteer.skills = data["skills"]

    if "availability" in data:
        volunteer.availability = data["availability"]

    if "status" in data:
        volunteer.status = data["status"]

    db.session.commit()

    return volunteer

def delete_volunteer(volunteer_id):

    volunteer = Volunteer.query.get(volunteer_id)

    if volunteer is None:
        return False

    db.session.delete(volunteer)
    db.session.commit()

    return True