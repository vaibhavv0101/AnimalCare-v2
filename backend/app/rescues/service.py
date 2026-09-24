from flask_jwt_extended import get_jwt_identity

from app.extensions import db
from app.models.animal import Animal
from app.models.rescue import Rescue
from app.models.user import User
from app.models.ngo import NGO
from app.models.volunteer import Volunteer
from app.models.notification import Notification

# ============================================================
# ASSIGN VOLUNTEER
# ============================================================

def assign_volunteer(rescue_id, volunteer_id):

    rescue = Rescue.query.get(rescue_id)

    if rescue is None:
        return None

    volunteer = Volunteer.query.get(volunteer_id)

    if volunteer is None:
        return False

    rescue.assigned_volunteer = volunteer.id

    notification = Notification(
        user_id=rescue.reported_by,
        title="Volunteer Assigned",
        message=(
            f"{volunteer.name} has been assigned "
            f"to your Rescue #{rescue.id}."
        )
    )

    db.session.add(notification)
    db.session.commit()

    return rescue




# ============================================================
# CREATE RESCUE
# ============================================================

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


# ============================================================
# GET ALL RESCUES
# ============================================================
def get_my_rescues():

    user_id = int(get_jwt_identity())

    return Rescue.query.filter_by(
        reported_by=user_id
    ).order_by(
        Rescue.created_at.desc()
    ).all()
def get_all_rescues():

    return Rescue.query.order_by(
        Rescue.created_at.desc()
    ).all()


# ============================================================
# GET RESCUE BY ID
# ============================================================

def get_rescue_by_id(rescue_id):

    return Rescue.query.get(rescue_id)


# ============================================================
# UPDATE RESCUE STATUS
# ============================================================

def update_rescue_status(rescue_id, data):

    rescue = Rescue.query.get(rescue_id)

    if rescue is None:
        return None

    new_status = data["status"]

    rescue.status = new_status

    notification = Notification(
        user_id=rescue.reported_by,
        title="Rescue Status Updated",
        message=(
            f"Your Rescue #{rescue.id} status "
            f"has been updated to {new_status}."
        ),
        
    )

    db.session.add(notification)

    db.session.commit()

    return rescue


# ============================================================
# ASSIGN NGO
# ============================================================

def assign_ngo(rescue_id, ngo_id):

    rescue = Rescue.query.get(rescue_id)

    if rescue is None:
        return None

    ngo = NGO.query.get(ngo_id)

    if ngo is None:
        return False

    rescue.assigned_ngo = ngo.id

    notification = Notification(
        user_id=rescue.reported_by,
        title="NGO Assigned",
        message=(
            f"{ngo.name} has been assigned "
            f"to your Rescue #{rescue.id}."
        ),
        notification_type="Rescue"
    )

    db.session.add(notification)
    db.session.commit()

    return rescue


# ============================================================
# DELETE RESCUE
# ============================================================

def delete_rescue(rescue_id):

    rescue = Rescue.query.get(rescue_id)

    if rescue is None:
        return False

    db.session.delete(rescue)
    db.session.commit()

    return True


# ============================================================
# ASSIGN RESCUE
# ============================================================

def assign_rescue(rescue_id, data):

    rescue = Rescue.query.get(rescue_id)

    if rescue is None:
        return None, "Rescue not found"

    # --------------------------------------------------------
    # Assign NGO
    # --------------------------------------------------------

    if "assigned_ngo" in data:

        ngo = NGO.query.get(
            data["assigned_ngo"]
        )

        if ngo is None:
            return None, "NGO not found"

        rescue.assigned_ngo = ngo.id

    # --------------------------------------------------------
    # Assign Volunteer
    # --------------------------------------------------------

    if "assigned_volunteer" in data:

        volunteer = Volunteer.query.get(
            data["assigned_volunteer"]
        )

        if volunteer is None:
            return None, "Volunteer not found"

        rescue.assigned_volunteer = volunteer.id

    # --------------------------------------------------------
    # Update Status
    # --------------------------------------------------------

    if "status" in data:

        rescue.status = data["status"]

    db.session.commit()

    return rescue, None