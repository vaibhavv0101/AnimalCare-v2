from datetime import datetime
from zoneinfo import ZoneInfo

from app.extensions import db


class Animal(db.Model):
    __tablename__ = "animals"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    species = db.Column(db.String(50), nullable=False)

    breed = db.Column(db.String(100))

    gender = db.Column(db.String(20))

    age = db.Column(db.Integer)

    color = db.Column(db.String(50))

    weight = db.Column(db.Float)

    rescue_location = db.Column(db.String(255))

    health_status = db.Column(db.String(100))

    vaccination_status = db.Column(db.String(100))

    description = db.Column(db.Text)

    image_url = db.Column(db.String(255))

    adoption_status = db.Column(
        db.String(50),
        default="Available"
    )

    created_at = db.Column(
    db.DateTime,
    default=lambda: datetime.now(ZoneInfo("Asia/Kolkata"))
    )
    
    rescues = db.relationship(
    "Rescue",
    back_populates="animal",
    cascade="all, delete-orphan"
    )
