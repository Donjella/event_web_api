from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

from init import db
from models.organiser import Organiser, organiser_schema, organisers_schema

organisers_bp = Blueprint("organisers", __name__, url_prefix="/organisers")

# Read all organisers - /organisers - GET
@organisers_bp.route("/")
def get_organisers():
    stmt = db.select(Organiser).order_by(Organiser.last_name, Organiser.first_name)
    organisers_list = db.session.scalars(stmt)
    return organisers_schema.dump(organisers_list)