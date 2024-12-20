from init import db, ma
from marshmallow import fields, validate

class Venue(db.Model):
    __tablename__ = "venues"

    venue_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)  
    street_address = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    postcode = db.Column(db.String(4), nullable=False)
  
    events = db.relationship("Event", back_populates="venue", cascade="all, delete-orphan", passive_deletes=True)

VALID_STATES_REGEX = r"(?i)^(WA|Western Australia|QLD|Queensland|VIC|Victoria|NSW|New South Wales|TAS|Tasmania|SA|South Australia)$"

class VenueSchema(ma.Schema):
    name = fields.String(
        required=True, 
        validate=validate.Length(min=3, error="Name must be at least 3 characters long.")
    )
    street_address = fields.String(
        required=True, 
        validate=validate.Length(min=5, error="Street address must be at least 5 characters long.")
    )
    city = fields.String(
        required=True, 
        validate=validate.Length(min=2, error="City must be at least 2 characters long.")
    )
    state = fields.String(
        required=True, 
        validate=validate.Regexp(VALID_STATES_REGEX, error="Invalid state. Must be a valid Australian state.")
    )  # Validate state using Regular Expressions
    postcode = fields.String(
        required=True, 
        validate=validate.Regexp(r"^\d{4}$", error="Postcode must be a 4-digit number.") 
    )  # Valid Australian postcodes
    capacity = fields.Integer(
        required=True, 
        validate=validate.Range(min=1, error="Capacity must be a positive number.")
    )  # Positive integer only

    events = fields.List(fields.Nested("EventSchema", exclude=["venue"]))  

    class Meta:
        fields = (
            "venue_id", 
            "name", 
            "street_address", 
            "city", 
            "state", 
            "postcode", 
            "capacity", 
            "events"
        )
        ordered = True

venue_schema = VenueSchema()
venues_schema = VenueSchema(many=True)
