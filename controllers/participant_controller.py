from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from marshmallow.exceptions import ValidationError

from init import db
from models.participant import Participant, participants_schema, participant_schema
from utils.error_handlers import format_validation_error, handle_unique_violation

participants_bp = Blueprint("participants", __name__, url_prefix="/participants")

# Create - /participants - POST
@participants_bp.route("/", methods=["POST"])
def create_participant():
    if not request.data or request.data.strip() == b"":
        return {"message": "Request body must not be empty"}, 400

    try:
        body_data = participant_schema.load(request.get_json())
        new_participant = Participant(
            first_name=body_data.get("first_name"),
            last_name=body_data.get("last_name"),
            email=body_data.get("email"),
            phone=body_data.get("phone")
        )
        db.session.add(new_participant)
        db.session.commit()
        return participant_schema.dump(new_participant), 201

    except ValidationError as err:
        return format_validation_error(err)

    except IntegrityError as err:
        return handle_unique_violation(err, body_data, ["email"])
    
# Read all - /participants - GET
@participants_bp.route("/", methods=["GET"])
def get_participants():
    stmt = db.select(Participant).order_by(Participant.first_name)
    participants_list = db.session.scalars(stmt)
    return participants_schema.dump(participants_list)

# Read one - /participants/<participant_id> - GET
@participants_bp.route("/<int:participant_id>", methods=["GET"])
def get_participant(participant_id):
    stmt = db.select(Participant).filter_by(participant_id=participant_id)
    participant = db.session.scalar(stmt)
    if participant:
        return participant_schema.dump(participant)
    else:
        return {"message": f"Participant with id {participant_id} not found"}, 404
    
# Update - /participants/<participant_id> - PUT/PATCH
@participants_bp.route("/<int:participant_id>", methods=["PUT", "PATCH"])
def update_participant(participant_id):
    if not request.data or request.data.strip() == b"":
        return {"message": "Request body must not be empty"}, 400

    stmt = db.select(Participant).filter_by(participant_id=participant_id)
    participant = db.session.scalar(stmt)
    if participant:
        try:
            body_data = participant_schema.load(request.get_json(), partial=True)
            participant.first_name = body_data.get("first_name", participant.first_name)
            participant.last_name = body_data.get("last_name", participant.last_name)
            participant.email = body_data.get("email", participant.email)
            participant.phone = body_data.get("phone", participant.phone)
            db.session.commit()
            return participant_schema.dump(participant), 200

        except ValidationError as err:
            return format_validation_error(err)

        except IntegrityError as err:
            return handle_unique_violation(err, body_data, ["email"])
    else:
        return {"message": f"Participant with id {participant_id} not found"}, 404
