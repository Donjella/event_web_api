from init import db, ma
from marshmallow import fields, validate

class EventParticipant(db.Model):
    __tablename__ = "event_participants"

    event_participant_id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey("events.event_id", ondelete="CASCADE"), nullable=False)
    participant_id = db.Column(db.Integer, db.ForeignKey("participants.participant_id", ondelete="CASCADE"), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # Changed to 'role'

    event = db.relationship("Event", back_populates="event_participants", passive_deletes=True)
    participant = db.relationship("Participant", back_populates="event_participants", passive_deletes=True)

VALID_ROLES = ("attendee", "speaker", "sponsor")  # Valid roles for an event participant

class EventParticipantSchema(ma.Schema):
    event = fields.Nested("EventSchema", exclude=["event_participants"])
    participant = fields.Nested("ParticipantSchema", exclude=["event_participants"])
    role = fields.String(
        required=True,
        validate=validate.OneOf(VALID_ROLES, error="Role must be 'attendee', 'speaker', or 'sponsor'.")
    )

    class Meta:
        fields = ("event_participant_id", "event_id", "participant_id", "role", "event", "participant")

event_participant_schema = EventParticipantSchema()
event_participants_schema = EventParticipantSchema(many=True)
