import os

from flask import Flask

from init import db, ma
from controllers.cli_controller import db_commands
from controllers.venue_controller import venues_bp
from controllers.organiser_controller import organisers_bp
from controllers.event_controller import events_bp
from controllers.participant_controller import participants_bp

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

    return app