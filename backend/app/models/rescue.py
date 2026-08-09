from datetime import datetime
from zoneinfo import ZoneInfo

from app.extensions import db


class Rescue(db.Model):
    __tablename__ = "rescues"

    id = db.Column(db.Integer, primary_key=True)

    animal_id = db.Column(
        db.Integer,
        db.ForeignKey("animals.id"),
        nullable=False
    )

    reported_by = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    assigned_ngo = db.Column(
        db.Integer,
        db.ForeignKey("users.id")
    )

    assigned_volunteer = db.Column(
        db.Integer,
        db.ForeignKey("users.id")
    )

    latitude = db.Column(db.Float)

    longitude = db.Column(db.Float)

    address = db.Column(db.String(255))

    priority = db.Column(
        db.String(30),
        default="Medium"
    )

    status = db.Column(
        db.String(30),
        default="Pending"
    )

    notes = db.Column(db.Text)

    created_at = db.Column(
    db.DateTime,
    default=lambda: datetime.now(ZoneInfo("Asia/Kolkata"))
    )

    updated_at = db.Column(
    db.DateTime,
    default=lambda: datetime.now(ZoneInfo("Asia/Kolkata")),
    onupdate=lambda: datetime.now(ZoneInfo("Asia/Kolkata"))
    )

    animal = db.relationship(
        "Animal",
        back_populates="rescues"
    )

    reporter = db.relationship(
        "User",
        foreign_keys=[reported_by],
        back_populates="reported_rescues"
    )

    volunteer = db.relationship(
        "User",
        foreign_keys=[assigned_volunteer],
        back_populates="assigned_rescues"
    )

    ngo = db.relationship(
        "User",
        foreign_keys=[assigned_ngo],
        back_populates="ngo_rescues"
    )