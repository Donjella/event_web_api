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
    if not request.data or request.data.strip() == b"":  
        return {"message": "Request body must be JSON and cannot be empty."}, 400

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
    
# Update - /events/<event_id> - PUT/PATCH
@events_bp.route("/<int:event_id>", methods=["PUT", "PATCH"])
def update_event(event_id):
    if not request.data or request.data.strip() == b"":  
        return {"message": "Request body must be JSON and cannot be empty"}, 400

    try:
        body_data = request.get_json()  
        if body_data is None:  
            return {"message": "Malformed JSON: Request body must be valid JSON"}, 400

        body_data = event_schema.load(body_data, partial=True)
    except ValidationError as err:
        return format_validation_error(err)

    stmt = db.select(Event).filter_by(event_id=event_id)
    event = db.session.scalar(stmt)
    if event:
        try:
            event.name = body_data.get("name") or event.name
            event.description = body_data.get("description") or event.description
            event.date = body_data.get("date") or event.date
            event.time = body_data.get("time") or event.time
            event.organiser_id = body_data.get("organiser_id") or event.organiser_id
            event.venue_id = body_data.get("venue_id") or event.venue_id
            db.session.commit()
            return event_schema.dump(event), 200
        except IntegrityError as err:
            return format_integrity_error(err)
    else:
        return {"message": f"Event with id {event_id} not found"}, 404

# Delete - /events/<event_id> - DELETE
@events_bp.route("/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    stmt = db.select(Event).filter_by(event_id=event_id)
    event = db.session.scalar(stmt)
    if event:
        db.session.delete(event)
        db.session.commit()
        return {"message": f"Event '{event.name}' deleted successfully"}, 200
    else:
        return {"message": f"Event with id {event_id} not found"}, 404
