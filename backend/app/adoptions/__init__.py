from flask import Blueprint

adoptions_bp = Blueprint(
    "adoptions",
    __name__,
    url_prefix="/api/adoptions"
)

from app.adoptions import routes