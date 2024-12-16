from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from marshmallow.exceptions import ValidationError

from init import db
from models.organiser import Organiser, organisers_schema, organiser_schema
from utils.error_handlers import format_validation_error, format_integrity_error

organisers_bp = Blueprint("organisers", __name__, url_prefix="/organisers")

# Read all - /organisers - GET
@organisers_bp.route("/", methods=["GET"])
def get_organisers():
    stmt = db.select(Organiser).order_by(Organiser.last_name, Organiser.first_name)
    organisers_list = db.session.scalars(stmt)
    return organisers_schema.dump(organisers_list)

# Read one - /organisers/<organiser_id> - GET
@organisers_bp.route("/<int:organiser_id>", methods=["GET"])
def get_organiser(organiser_id):
    stmt = db.select(Organiser).filter_by(organiser_id=organiser_id)
    organiser = db.session.scalar(stmt)
    if organiser:
        return organiser_schema.dump(organiser)
    else:
        return {"message": f"Organiser with id {organiser_id} not found"}, 404

# Create - /organisers - POST
@organisers_bp.route("/", methods=["POST"])
def create_organiser():
    if not request.json:
        return {"message": "Request body must be JSON"}, 400

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

    except ValidationError as err:
        return format_validation_error(err)

    except IntegrityError as err:
        return format_integrity_error(err)

# Update - /organisers/<organiser_id> - PUT/PATCH
@organisers_bp.route("/<int:organiser_id>", methods=["PUT", "PATCH"])
def update_organiser(organiser_id):
    if not request.json:
        return {"message": "Request body must be JSON"}, 400

    stmt = db.select(Organiser).filter_by(organiser_id=organiser_id)
    organiser = db.session.scalar(stmt)
    if organiser:
        try:
            body_data = organiser_schema.load(request.get_json(), partial=True)
            organiser.first_name = body_data.get("first_name") or organiser.first_name
            organiser.last_name = body_data.get("last_name") or organiser.last_name
            organiser.company_name = body_data.get("company_name") or organiser.company_name
            organiser.email = body_data.get("email") or organiser.email
            organiser.phone = body_data.get("phone") or organiser.phone
            db.session.commit()
            return organiser_schema.dump(organiser), 200

        except ValidationError as err:
            return format_validation_error(err)

        except IntegrityError as err:
            return format_integrity_error(err)

    else:
        return {"message": f"Organiser with id {organiser_id} not found"}, 404

# Delete - /organisers/<organiser_id> - DELETE
@organisers_bp.route("/<int:organiser_id>", methods=["DELETE"])
def delete_organiser(organiser_id):
    stmt = db.select(Organiser).filter_by(organiser_id=organiser_id)
    organiser = db.session.scalar(stmt)
    if organiser:
        db.session.delete(organiser)
        db.session.commit()
        return {"message": f"Organiser '{organiser.first_name} {organiser.last_name}' deleted successfully"}, 200
    else:
        return {"message": f"Organiser with id {organiser_id} not found"}, 404
