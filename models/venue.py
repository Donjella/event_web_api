from init import db, ma
from marshmallow import fields

class Venue(db.Model):
    __tablename__ = 'venues'
    venue_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    capacity = db.Column(db.Integer)

class VenueSchema(ma.Schema):
    class Meta:
        fields = ("venue_id", "name", "location", "capacity")

venue_schema = VenueSchema()
venues_schema = VenueSchema(many=True)
