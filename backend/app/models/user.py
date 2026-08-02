from datetime import datetime

from app.extensions import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    full_name = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    phone = db.Column(db.String(20), unique=True)

    password = db.Column(db.String(255), nullable=False)

    profile_image = db.Column(db.String(255))

    is_verified = db.Column(db.Boolean, default=False)

    is_active = db.Column(db.Boolean, default=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    role_id = db.Column(
        db.Integer,
        db.ForeignKey("roles.id"),
        nullable=False,
    )

    role = db.relationship("Role", back_populates="users")

    def __repr__(self):
        return f"<User {self.email}>"
    
    reported_rescues = db.relationship(
    "Rescue",
    foreign_keys="Rescue.reported_by",
    back_populates="reporter"
    )
    assigned_rescues = db.relationship(
    "Rescue",
    foreign_keys="Rescue.assigned_volunteer",
    back_populates="volunteer"
    )
    ngo_rescues = db.relationship(
    "Rescue",
    foreign_keys="Rescue.assigned_ngo",
    back_populates="ngo"
    )
  

    


  