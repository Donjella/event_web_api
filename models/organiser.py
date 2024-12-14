from init import db, ma
from marshmallow import fields

class Organiser(db.Model):
    __tablename__ = "organisers"

    organiser_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    company_name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20))

    # Use a string reference to the Event class
    events = db.relationship("Event", back_populates="organiser", cascade="all, delete")

class OrganiserSchema(ma.Schema):
    events = fields.List(fields.Nested("EventSchema"), exclude=["organiser"])

    class Meta:
        fields = ("organiser_id", "first_name", "last_name", "company_name", "email", "phone", "events")

organiser_schema = OrganiserSchema()
organisers_schema = OrganiserSchema(many=True)
