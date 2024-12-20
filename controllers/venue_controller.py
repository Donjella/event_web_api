from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from marshmallow.exceptions import ValidationError

from init import db
from models.venue import Venue, venues_schema, venue_schema
from utils.error_handlers import format_validation_error, handle_unique_violation

venues_bp = Blueprint("venues", __name__, url_prefix="/venues")

# Read all - /venues - GET
@venues_bp.route("/", methods=["GET"])
def get_venues():
    stmt = db.select(Venue).order_by(Venue.name)
    venues_list = db.session.scalars(stmt)
    return venues_schema.dump(venues_list)

# Read one - /venues/<venue_id> - GET
@venues_bp.route("/<int:venue_id>", methods=["GET"])
def get_venue(venue_id):
    stmt = db.select(Venue).filter_by(venue_id=venue_id)
    venue = db.session.scalar(stmt)
    if venue:
        return venue_schema.dump(venue)
    else:
        return {"message": f"Venue with id {venue_id} not found"}, 404

# Create - /venues - POST
@venues_bp.route("/", methods=["POST"])
def create_venue():
    if not request.data or request.data.strip() == b"":
        return {"message": "Request body must be JSON and cannot be empty."}, 400

    try:
        body_data = venue_schema.load(request.get_json())
        new_venue = Venue(
            name=body_data.get("name"),
            street_address=body_data.get("street_address"),
            city=body_data.get("city"),
            state=body_data.get("state"),
            postcode=body_data.get("postcode"),
            capacity=body_data.get("capacity")
        )
        db.session.add(new_venue)
        db.session.commit()
        return venue_schema.dump(new_venue), 201

    except ValidationError as err:
        return format_validation_error(err)

    except IntegrityError as err:
        return handle_unique_violation(err, body_data, ["name"])

# Update - /venues/<venue_id> - PUT/PATCH
@venues_bp.route("/<int:venue_id>", methods=["PUT", "PATCH"])
def update_venue(venue_id):
    if not request.data or request.data.strip() == b"":
        return {"message": "Request body must be JSON and cannot be empty."}, 400

    stmt = db.select(Venue).filter_by(venue_id=venue_id)
    venue = db.session.scalar(stmt)
    if venue:
        try:
            body_data = venue_schema.load(request.get_json(), partial=True)
            venue.name = body_data.get("name") or venue.name
            venue.street_address = body_data.get("street_address") or venue.street_address
            venue.city = body_data.get("city") or venue.city
            venue.state = body_data.get("state") or venue.state
            venue.postcode = body_data.get("postcode") or venue.postcode
            venue.capacity = body_data.get("capacity") or venue.capacity
            db.session.commit()
            return venue_schema.dump(venue), 200

        except ValidationError as err:
            return format_validation_error(err)

        except IntegrityError as err:
            return handle_unique_violation(err, body_data, ["name"])
    else:
        return {"message": f"Venue with id {venue_id} not found"}, 404

# Delete - /venues/<venue_id> - DELETE
@venues_bp.route("/<int:venue_id>", methods=["DELETE"])
def delete_venue(venue_id):
    stmt = db.select(Venue).filter_by(venue_id=venue_id)
    venue = db.session.scalar(stmt)
    if venue:
        db.session.delete(venue)
        db.session.commit()
        return {"message": f"Venue '{venue.name}' deleted successfully"}, 200
    else:
        return {"message": f"Venue with id {venue_id} not found"}, 404

