from flask import request, jsonify
from flask_jwt_extended import jwt_required

from app.donations import donations_bp
from app.donations.schemas import DonationSchema
from app.donations.service import (
    create_donation,
    get_my_donations,
    get_all_donations,
    get_donation_by_id,
    update_donation_status,
    delete_donation
)
from app.auth.decorators import role_required


schema = DonationSchema()


# ============================================================
# HELPER - CONVERT DONATION TO JSON
# ============================================================

def donation_to_dict(donation):

    return {
        "id": donation.id,
        "user_id": donation.user_id,

        "donor_name": (
            "Anonymous"
            if donation.is_anonymous
            else donation.donor_name
        ),

        "email": donation.email,
        "phone": donation.phone,
        "amount": float(donation.amount),
        "purpose": donation.purpose,
        "payment_reference": donation.payment_reference,
        "payment_status": donation.payment_status,
        "is_anonymous": donation.is_anonymous,

        "created_at": (
            donation.created_at.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            if donation.created_at
            else None
        )
    }


# ============================================================
# CREATE DONATION
# LOGGED-IN USER
# ============================================================

@donations_bp.route("/", methods=["POST"])
@jwt_required()
def add_donation():

    data = request.get_json(silent=True) or {}

    errors = schema.validate(data)

    if errors:
        return jsonify({
            "success": False,
            "errors": errors
        }), 400

    donation = create_donation(data)

    return jsonify({
        "success": True,
        "message": "Donation submitted successfully",
        "donation_id": donation.id,
        "status": donation.payment_status
    }), 201


# ============================================================
# GET MY DONATIONS
# LOGGED-IN USER
# ============================================================

@donations_bp.route("/my", methods=["GET"])
@jwt_required()
def my_donations():

    donations = get_my_donations()

    result = [
        donation_to_dict(donation)
        for donation in donations
    ]

    return jsonify({
        "success": True,
        "count": len(result),
        "donations": result
    }), 200


# ============================================================
# GET ALL DONATIONS
# ADMIN ONLY
# ============================================================

@donations_bp.route("/", methods=["GET"])
@jwt_required()
@role_required("Admin")
def list_donations():

    donations = get_all_donations()

    result = [
        donation_to_dict(donation)
        for donation in donations
    ]

    return jsonify({
        "success": True,
        "count": len(result),
        "donations": result
    }), 200


# ============================================================
# GET SINGLE DONATION
# ADMIN ONLY
# ============================================================

@donations_bp.route(
    "/<int:donation_id>",
    methods=["GET"]
)
@jwt_required()
@role_required("Admin")
def donation_details(donation_id):

    donation = get_donation_by_id(donation_id)

    if donation is None:

        return jsonify({
            "success": False,
            "message": "Donation not found"
        }), 404

    return jsonify({
        "success": True,
        "donation": donation_to_dict(donation)
    }), 200


# ============================================================
# UPDATE DONATION STATUS
# ADMIN ONLY
# ============================================================

@donations_bp.route(
    "/<int:donation_id>/status",
    methods=["PUT"]
)
@jwt_required()
@role_required("Admin")
def change_donation_status(donation_id):

    data = request.get_json(silent=True) or {}

    status = data.get("status")

    allowed_statuses = [
        "Pending",
        "Received",
        "Cancelled"
    ]

    if status not in allowed_statuses:

        return jsonify({
            "success": False,
            "message": (
                "Status must be Pending, "
                "Received or Cancelled"
            )
        }), 400

    donation = update_donation_status(
        donation_id,
        status
    )

    if donation is None:

        return jsonify({
            "success": False,
            "message": "Donation not found"
        }), 404

    return jsonify({
        "success": True,
        "message": "Donation status updated successfully",
        "donation_id": donation.id,
        "status": donation.payment_status
    }), 200


# ============================================================
# DELETE DONATION
# ADMIN ONLY
# ============================================================

@donations_bp.route(
    "/<int:donation_id>",
    methods=["DELETE"]
)
@jwt_required()
@role_required("Admin")
def remove_donation(donation_id):

    deleted = delete_donation(donation_id)

    if not deleted:

        return jsonify({
            "success": False,
            "message": "Donation not found"
        }), 404

    return jsonify({
        "success": True,
        "message": "Donation deleted successfully"
    }), 200