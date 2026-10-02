from flask_jwt_extended import get_jwt_identity

from app.extensions import db
from app.models.donation import Donation


# ============================================================
# CREATE DONATION
# ============================================================

def create_donation(data):

    user_id = int(get_jwt_identity())

    donation = Donation(
        user_id=user_id,
        donor_name=data["donor_name"],
        email=data["email"],
        phone=data.get("phone"),
        amount=data["amount"],
        purpose=data["purpose"],
        payment_reference=data.get("payment_reference"),
        payment_status="Pending",
        is_anonymous=data.get("is_anonymous", False)
    )

    db.session.add(donation)
    db.session.commit()

    return donation


# ============================================================
# GET LOGGED-IN USER DONATIONS
# ============================================================

def get_my_donations():

    user_id = int(get_jwt_identity())

    return (
        Donation.query
        .filter_by(user_id=user_id)
        .order_by(Donation.created_at.desc())
        .all()
    )


# ============================================================
# GET ALL DONATIONS
# ADMIN
# ============================================================

def get_all_donations():

    return (
        Donation.query
        .order_by(Donation.created_at.desc())
        .all()
    )


# ============================================================
# GET SINGLE DONATION
# ============================================================

def get_donation_by_id(donation_id):

    return db.session.get(
        Donation,
        donation_id
    )


# ============================================================
# UPDATE DONATION STATUS
# ADMIN
# ============================================================

def update_donation_status(donation_id, status):

    donation = db.session.get(
        Donation,
        donation_id
    )

    if donation is None:
        return None

    donation.payment_status = status

    db.session.commit()

    return donation


# ============================================================
# DELETE DONATION
# ADMIN
# ============================================================

def delete_donation(donation_id):

    donation = db.session.get(
        Donation,
        donation_id
    )

    if donation is None:
        return False

    db.session.delete(donation)
    db.session.commit()

    return True