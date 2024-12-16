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

# Create a new organiser - /organisers - POST
@organisers_bp.route("/", methods=["POST"])
def create_organiser():
    try:
        body_data = organiser_schema.load(request.get_json())
        new_organiser = Organiser(
            first_name=body_data.get("first_name"),
            last_name=body_data.get("last_name"),
            company_name=body_data.get("company_name"),
            email=body_data.get("email"),
            phone=body_data.get("phone")
        )
        db.session.add(new_organiser)
        db.session.commit()
        return organiser_schema.dump(new_organiser), 201
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"message": f"Email '{body_data.get('email')}' is already in use"}, 409
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"message": f"The field '{err.orig.diag.column_name}' is required"}, 409