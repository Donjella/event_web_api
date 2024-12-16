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

