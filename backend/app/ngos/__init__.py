from flask import Blueprint

ngos_bp = Blueprint(
    "ngos",
    __name__,
    url_prefix="/api/ngos"
)

from app.ngos import routes