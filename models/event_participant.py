from init import db, ma
from marshmallow import fields, validate


class EventParticipant(db.Model):
    __tablename__ = "event_participants"

    event_participant_id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey("events.event_id", ondelete="CASCADE"), nullable=False)
    participant_id = db.Column(db.Integer, db.ForeignKey("participants.participant_id", ondelete="CASCADE"), nullable=False)
    role = db.Column(db.String(50), nullable=False)

    __table_args__ = (db.UniqueConstraint("event_id", "participant_id", name="uq_event_participant"),)

    event = db.relationship("Event", back_populates="event_participants", passive_deletes=True)
    participant = db.relationship("Participant", back_populates="event_participants", passive_deletes=True)


class EventParticipantSchema(ma.Schema):
    role = fields.String(
        required=True,
        validate=validate.OneOf(
            ["attendee", "speaker", "sponsor"],
            error="Role must be one of: 'attendee', 'speaker', or 'sponsor'."
        )
    )
    event = fields.Nested(
        "EventSchema",
        exclude=["event_id", "organiser_id", "venue_id", "time", "venue", "event_participants"]
    )
    participant = fields.Nested(
        "ParticipantSchema",
        exclude=["participant_id", "event_participants"]
    )

    class Meta:
        fields = ("event_participant_id", "role", "event", "participant")


event_participant_schema = EventParticipantSchema()
event_participants_schema = EventParticipantSchema(many=True)
