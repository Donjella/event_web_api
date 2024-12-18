from init import db, ma
from marshmallow import fields


class Participant(db.Model):
    __tablename__ = "participants"

    participant_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)

    event_participants = db.relationship("EventParticipant", back_populates="participant", cascade="all, delete-orphan", passive_deletes=True)


class ParticipantSchema(ma.Schema):
    event_participants = fields.List(
        fields.Nested("EventParticipantSchema", exclude=["participant"])
    )

    class Meta:
        fields = ("participant_id", "first_name", "last_name", "email", "phone", "event_participants")


participant_schema = ParticipantSchema()
participants_schema = ParticipantSchema(many=True)
