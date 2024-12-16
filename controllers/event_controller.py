from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from marshmallow.exceptions import ValidationError
from datetime import datetime

from init import db
from models.event import Event, events_schema, event_schema
from utils.error_handlers import format_validation_error, format_integrity_error

events_bp = Blueprint("events", __name__, url_prefix="/events")

# Create - /events - POST
@events_bp.route("/", methods=["POST"])
def create_event():
    if not request.json:
        return {"message": "Request body must be JSON"}, 400

    try:
        body_data = event_schema.load(request.get_json())
        new_event = Event(
            name=body_data.get("name"),
            description=body_data.get("description"),
            date=body_data.get("date"),
            time=body_data.get("time"),
            organiser_id=body_data.get("organiser_id"),
            venue_id=body_data.get("venue_id")
        )
        db.session.add(new_event)
        db.session.commit()
        return event_schema.dump(new_event), 201

    except ValidationError as err:
        return format_validation_error(err)

    except IntegrityError as err:
        return format_integrity_error(err)

# Read all - /events - GET
@events_bp.route("/", methods=["GET"])
def get_events():
    stmt = db.select(Event).order_by(Event.date, Event.time)
    events_list = db.session.scalars(stmt)
    return events_schema.dump(events_list), 200

# Read one - /events/<event_id> - GET
@events_bp.route("/<int:event_id>", methods=["GET"])
def get_event(event_id):
    stmt = db.select(Event).filter_by(event_id=event_id)
    event = db.session.scalar(stmt)
    if event:
        return event_schema.dump(event), 200
    else:
        return {"message": f"Event with id {event_id} not found"}, 404