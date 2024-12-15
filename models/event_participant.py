from init import db, ma
from marshmallow import fields

class EventParticipant(db.Model):
    __tablename__ = "event_participants"

    event_participant_id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey("events.event_id", ondelete="CASCADE"), nullable=False)
    participant_id = db.Column(db.Integer, db.ForeignKey("participants.participant_id", ondelete="CASCADE"), nullable=False)
    registration_date = db.Column(db.Date, nullable=False)

    event = db.relationship("Event", back_populates="event_participants", passive_deletes=True)
    participant = db.relationship("Participant", back_populates="event_participants", passive_deletes=True)

class EventParticipantSchema(ma.Schema):
    event = fields.Nested("EventSchema", exclude=["event_participants"])
    participant = fields.Nested("ParticipantSchema", exclude=["event_participants"])

    class Meta:
        fields = ("event_participant_id", "event_id", "participant_id", "registration_date", "event", "participant")

event_participant_schema = EventParticipantSchema()
event_participants_schema = EventParticipantSchema(many=True)
