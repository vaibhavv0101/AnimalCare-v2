
import os
from decimal import Decimal, InvalidOperation

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from app.donations.demo.payment_simulator import simulate_payment


demo_payments_bp = Blueprint(
    "demo_payments",
    __name__,
    url_prefix="/api/donations/demo"
)


@demo_payments_bp.route("/simulate", methods=["POST"])
@jwt_required()
def simulate_donation_payment():

    # Demo payments are disabled unless explicitly enabled.
    if os.getenv("ANIMALCARE_DEMO_PAYMENTS") != "true":
        return jsonify({
            "success": False,
            "message": "Demo payments are disabled"
        }), 403

    data = request.get_json(silent=True) or {}

    if not isinstance(data, dict):
        return jsonify({
            "success": False,
            "message": "Invalid JSON request"
        }), 400

    try:
        amount = Decimal(str(data.get("amount")))
    except (InvalidOperation, TypeError, ValueError):
        return jsonify({
            "success": False,
            "message": "Invalid donation amount"
        }), 400

    outcome = data.get("outcome", "success")

    try:
        result = simulate_payment(amount, outcome)
    except ValueError as error:
        return jsonify({
            "success": False,
            "message": str(error)
        }), 400

    return jsonify({
        "success": True,
        "simulation": result,
        "notice": "DEMO ONLY - NO REAL MONEY TRANSFERRED"
    }), 200
