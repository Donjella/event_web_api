from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

from init import db
from models.venue import Venue, venues_schema, venue_schema

venues_bp = Blueprint("venues", __name__, url_prefix="/venues")

# Read all - /venues - GET
@venues_bp.route("/")
def get_venues():
    stmt = db.select(Venue).order_by(Venue.name)
    venues_list = db.session.scalars(stmt)
    return venues_schema.dump(venues_list)

# Read one - /venues/<venue_id> - GET
@venues_bp.route("/<int:venue_id>")
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
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"message": f"The field '{err.orig.diag.column_name}' is required"}, 400
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"message": "Venue name must be unique"}, 400

# Delete - /venues/<venue_id> - DELETE
@venues_bp.route("/<int:venue_id>", methods=["DELETE"])
def delete_venue(venue_id):
    stmt = db.select(Venue).filter_by(venue_id=venue_id)
    venue = db.session.scalar(stmt)
    if venue:
        db.session.delete(venue)
        db.session.commit()
        return {"message": f"Venue '{venue.name}' deleted successfully"}
    else:
        return {"message": f"Venue with id {venue_id} not found"}, 404