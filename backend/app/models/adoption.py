from datetime import datetime
from app.extensions import db


class Adoption(db.Model):
    __tablename__ = "adoptions"

    id = db.Column(db.Integer, primary_key=True)

    animal_id = db.Column(
        db.Integer,
        db.ForeignKey("animals.id"),
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    reason = db.Column(db.Text)

    phone = db.Column(db.String(20))

    address = db.Column(db.String(255))

    occupation = db.Column(db.String(100))

    status = db.Column(
        db.String(30),
        default="Pending"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )