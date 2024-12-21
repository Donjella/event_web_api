from init import db, ma
from marshmallow import fields, validate

class Organiser(db.Model):
    __tablename__ = "organisers"

    organiser_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    company_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)

    events = db.relationship("Event", back_populates="organiser", cascade="all, delete-orphan", passive_deletes=True)

# Australian phone number regex
AU_PHONE_REGEX = r"^\+61[2-9]\d{8}$|^0[2-9]\d{8}$"

class OrganiserSchema(ma.Schema):
    first_name = fields.String(
        required=True, 
        validate=validate.Length(min=1, max=50, error="First name must be between 1 and 50 characters long.")
    )
    last_name = fields.String(
        required=True, 
        validate=validate.Length(min=1, max=50, error="Last name must be between 1 and 50 characters long.")
    )
    company_name = fields.String(
        required=True,
        validate=validate.Length(max=100, error="Company name cannot exceed 100 characters.")
    )
    email = fields.Email(
        required=True, 
        error_messages={"required": "Email is required.", "invalid": "Invalid email address format."}
    )
    phone = fields.String(
        required=True, 
        validate=validate.Regexp(AU_PHONE_REGEX, error="Phone must be a valid Australian number (e.g., +614XXXXXXXX or 04XXXXXXXX).")
    )

    events = fields.List(fields.Nested("EventSchema", exclude=["organiser_id", "event_participants"]))

    class Meta:
        fields = ("organiser_id", "first_name", "last_name", "company_name", "email", "phone", "events")
        ordered = True

organiser_schema = OrganiserSchema()
organisers_schema = OrganiserSchema(many=True)
