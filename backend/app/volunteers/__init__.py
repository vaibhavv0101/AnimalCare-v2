from flask import Blueprint

volunteers_bp = Blueprint(
    "volunteers",
    __name__,
    url_prefix="/api/volunteers"
)

from app.volunteers import routes