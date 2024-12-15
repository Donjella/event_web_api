from init import db, ma
from marshmallow import fields

class Venue(db.Model):
    __tablename__ = "venues"
    
    venue_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    street_address = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    postcode = db.Column(db.String(20), nullable=False)
    capacity = db.Column(db.Integer)

    events = db.relationship("Event", back_populates="venue", cascade="all, delete")

class VenueSchema(ma.Schema):
    events = fields.List(fields.Nested("EventSchema", exclude=["venue"]))

    class Meta:
        fields = ("venue_id", "name", "street_address", "city", "state", "postcode", "capacity", "events")

venue_schema = VenueSchema()
venues_schema = VenueSchema(many=True)
