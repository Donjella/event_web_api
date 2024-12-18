from psycopg2 import errorcodes
from marshmallow.exceptions import ValidationError

def format_validation_error(err: ValidationError):
    return {"message": "Validation error", "details": err.messages}, 400

def format_integrity_error(err):
    if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
        return {"message": "A unique constraint was violated"}, 400
    if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
        return {"message": f"The field '{err.orig.diag.column_name}' is required"}, 400
    return {"message": "A database error occurred"}, 500

def handle_unique_violation(err, body_data, fields):
    if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
        if "uq_event_participant" in err.orig.diag.constraint_name:
            return {
                "message": f"The participant with ID {body_data.get('participant_id')} is already registered for event ID {body_data.get('event_id')}"
            }, 400
        for field in fields:
            if field in err.orig.diag.constraint_name:
                value = body_data.get(field, "unknown")
                return {"message": f"The value for '{field}' ('{value}') must be unique"}, 400
    return {"message": "A unique constraint was violated, but the field could not be determined"}, 400
