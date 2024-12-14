from init import db, ma
from marshmallow import fields

# Avoid circular imports
from models.organiser import Organiser

class Event(db.Model):
    __tablename__ = 'events'
    event_id = db.Column(db.Integer, primary_key=True)
    organiser_id = db.Column(db.Integer, db.ForeignKey('organisers.organiser_id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.venue_id'), nullable=False)  # Assuming you have a Venue model with venue_id as primary key
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    organiser = db.relationship("Organiser", back_populates="events")

class EventSchema(ma.Schema):
    organiser = fields.Nested("OrganiserSchema", exclude=["events"])

    class Meta:
        fields = ("event_id", "organiser_id", "venue_id", "name", "description", "date", "time", "organiser")

event_schema = EventSchema()
events_schema = EventSchema(many=True)
