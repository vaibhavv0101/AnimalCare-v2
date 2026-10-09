
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from uuid import uuid4


def simulate_payment(amount, outcome="success"):
    """
    Simulate a donation payment.
    No real payment gateway or bank is involved.
    """

    try:
        amount = Decimal(str(amount))
    except (InvalidOperation, ValueError, TypeError):
        raise ValueError("Invalid donation amount")

    if not amount.is_finite() or amount <= 0:
        raise ValueError("Amount must be greater than zero")

    if amount.as_tuple().exponent < -2:
        raise ValueError("Maximum two decimal places allowed")

    if outcome not in ("success", "failed"):
        raise ValueError("Invalid demo payment outcome")

    return {
        "demo": True,
        "real_payment": False,
        "transaction_id": f"DEMO-{uuid4().hex[:12].upper()}",
        "amount": str(amount),
        "currency": "INR",
        "payment_status": (
            "Demo Success"
            if outcome == "success"
            else "Demo Failed"
        ),
        "created_at": datetime.now(
            timezone.utc
        ).isoformat(),
        "message": "SIMULATION ONLY - NO REAL MONEY TRANSFERRED"
    }
