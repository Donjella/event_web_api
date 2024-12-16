from init import db, ma
from marshmallow import fields, validate
from datetime import datetime

class Event(db.Model):
    __tablename__ = "events"

    event_id = db.Column(db.Integer, primary_key=True)
    organiser_id = db.Column(db.Integer, db.ForeignKey("organisers.organiser_id", ondelete="CASCADE"), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey("venues.venue_id", ondelete="CASCADE"), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)

    organiser = db.relationship("Organiser", back_populates="events", passive_deletes=True)
    venue = db.relationship("Venue", back_populates="events", passive_deletes=True)
    event_participants = db.relationship("EventParticipant", back_populates="event", cascade="all, delete-orphan")

class EventSchema(ma.Schema):
    name = fields.String(
        required=True,
        validate=validate.Length(min=3, error="Event name must be at least 3 characters long.")
    )
    description = fields.String(
        validate=validate.Length(max=255, error="Description cannot exceed 255 characters.")
    )
    date = fields.Date(
        required=True,
        validate=validate.Range(
            min=datetime.today().date(),
            error="Event date must be today or in the future."
        )
    )
    time = fields.Time(required=True)
    organiser_id = fields.Integer(required=True)
    venue_id = fields.Integer(required=True)

    organiser = fields.Nested("OrganiserSchema", exclude=["events"])
    venue = fields.Nested("VenueSchema", exclude=["events"])
    event_participants = fields.List(fields.Nested("EventParticipantSchema", exclude=["event"]))

    class Meta:
        fields = (
            "event_id", 
            "organiser_id", 
            "venue_id", 
            "name", 
            "description", 
            "date", 
            "time", 
            "organiser", 
            "venue", 
            "event_participants"
        )

event_schema = EventSchema()
events_schema = EventSchema(many=True)
