from flask import Blueprint

animals_bp = Blueprint(
    "animals",
    __name__,
    url_prefix="/api/animals"
)

from app.animals import routes