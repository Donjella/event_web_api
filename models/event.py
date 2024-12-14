from init import db, ma
from marshmallow import fields

class Event(db.Model):
    __tablename__ = 'events'
    event_id = db.Column(db.Integer, primary_key=True)
    organiser_id = db.Column(db.Integer, db.ForeignKey('organisers.organiser_id', ondelete='CASCADE'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.venue_id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)

    organiser = db.relationship("Organiser", back_populates="events")
    venue = db.relationship("Venue", back_populates="events")
    event_participants = db.relationship("EventParticipant", back_populates="event", cascade="all, delete")

class EventSchema(ma.Schema):
    organiser = fields.Nested("OrganiserSchema", exclude=["events"])
    venue = fields.Nested("VenueSchema", exclude=["events"])
    event_participants = fields.List(fields.Nested("EventParticipantSchema", exclude=["event"]))

    class Meta:
        fields = ("event_id", "organiser_id", "venue_id", "name", "description", "date", "time", "organiser", "venue", "event_participants")

event_schema = EventSchema()
events_schema = EventSchema(many=True)
