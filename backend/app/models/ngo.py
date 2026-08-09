from datetime import datetime
from zoneinfo import ZoneInfo

from app.extensions import db


class NGO(db.Model):
    __tablename__ = "ngos"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String(150),
        nullable=False
    )

    email = db.Column(
        db.String(150),
        unique=True,
        nullable=False
    )

    phone = db.Column(
        db.String(20),
        nullable=False
    )

    address = db.Column(
        db.String(255),
        nullable=False
    )

    registration_number = db.Column(
        db.String(100),
        unique=True
    )

    description = db.Column(
        db.Text
    )

    status = db.Column(
        db.String(30),
        default="Active"
    )

    created_at = db.Column(
    db.DateTime,
    default=lambda: datetime.now(ZoneInfo("Asia/Kolkata"))
    )