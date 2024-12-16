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

# Read one organiser - /organisers/<id> - GET
@organisers_bp.route("/<int:organiser_id>")
def get_organiser(organiser_id):
    stmt = db.select(Organiser).filter_by(organiser_id=organiser_id)
    organiser = db.session.scalar(stmt)
    if organiser:
        return organiser_schema.dump(organiser)
    else:
        return {"message": f"Organiser with id {organiser_id} does not exist"}, 404