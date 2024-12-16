from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from marshmallow.exceptions import ValidationError
from datetime import datetime

from init import db
from models.event import Event, events_schema, event_schema
from utils.error_handlers import format_validation_error, format_integrity_error

events_bp = Blueprint("events", __name__, url_prefix="/events")

# Read all - /events - GET
@events_bp.route("/", methods=["GET"])
def get_events():
    stmt = db.select(Event).order_by(Event.date, Event.time)
    events_list = db.session.scalars(stmt)
    return events_schema.dump(events_list), 200