from datetime import datetime
from zoneinfo import ZoneInfo

from app.extensions import db


class Donation(db.Model):
    __tablename__ = "donations"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # Logged-in AnimalCare user
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    donor_name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        nullable=False
    )

    phone = db.Column(
        db.String(20)
    )

    amount = db.Column(
        db.Numeric(10, 2),
        nullable=False
    )

    purpose = db.Column(
        db.String(100),
        nullable=False
    )

    payment_reference = db.Column(
        db.String(150)
    )

    payment_status = db.Column(
        db.String(30),
        default="Pending",
        nullable=False
    )

    is_anonymous = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(
            ZoneInfo("Asia/Kolkata")
        )
    )

    def __repr__(self):
        return f"<Donation {self.id} - {self.amount}>"