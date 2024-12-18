import os

from flask import Flask

from init import db, ma
from controllers.cli_controller import db_commands
from controllers.venue_controller import venues_bp
from controllers.organiser_controller import organisers_bp
from controllers.event_controller import events_bp
from controllers.participant_controller import participants_bp
from controllers.event_participant_controller import event_participants_bp

# Application factory - idea is to set up the application in a function.
def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI")

    db.init_app(app)
    ma.init_app(app)

    app.register_blueprint(db_commands)
    app.register_blueprint(venues_bp)
    app.register_blueprint(organisers_bp)
    app.register_blueprint(events_bp)
    app.register_blueprint(participants_bp)
    app.register_blueprint(event_participants_bp)

    # Global Error Handlers
    @app.errorhandler(400)
    def bad_request(err):
        return {"message": "Bad Request", "details": str(err)}, 400

    @app.errorhandler(404)
    def not_found(err):
        return {"message": "Not Found", "details": str(err)}, 404

    @app.errorhandler(500)
    def internal_server_error(err):
        return {"message": "Internal Server Error", "details": str(err)}, 500

    return app