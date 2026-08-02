from flask import Blueprint

rescues_bp = Blueprint(
    "rescues",
    __name__,
    url_prefix="/api/rescues"
)

from app.rescues import routes