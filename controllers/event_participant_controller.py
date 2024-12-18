from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from marshmallow.exceptions import ValidationError

from init import db
from models.event_participant import EventParticipant, event_participants_schema, event_participant_schema
from utils.error_handlers import format_validation_error, handle_unique_violation

event_participants_bp = Blueprint("event_participants", __name__, url_prefix="/event_participants")

# Read all - /event_participants - GET
@event_participants_bp.route("/", methods=["GET"])
def get_event_participants():
    stmt = db.select(EventParticipant).order_by(EventParticipant.event_participant_id)
    event_participants_list = db.session.scalars(stmt)
    return event_participants_schema.dump(event_participants_list)

# Read one - /event_participants/<event_participant_id> - GET
@event_participants_bp.route("/<int:event_participant_id>", methods=["GET"])
def get_event_participant(event_participant_id):
    stmt = db.select(EventParticipant).filter_by(event_participant_id=event_participant_id)
    event_participant = db.session.scalar(stmt)
    if event_participant:
        return event_participant_schema.dump(event_participant)
    else:
        return {"message": f"Event Participant with id {event_participant_id} not found"}, 404

