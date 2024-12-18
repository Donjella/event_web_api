from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from marshmallow.exceptions import ValidationError

from init import db
from models.participant import Participant, participants_schema, participant_schema
from utils.error_handlers import format_validation_error, format_integrity_error

participants_bp = Blueprint("participants", __name__, url_prefix="/participants")

# Read all - /participants - GET
@participants_bp.route("/", methods=["GET"])
def get_participants():
    stmt = db.select(Participant).order_by(Participant.first_name)
    participants_list = db.session.scalars(stmt)
    return participants_schema.dump(participants_list)