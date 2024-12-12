import os

from flask import Flask

from init import db, ma

# Application factory - idea is to set up the application in a function.
def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI")

    db.init_app(app)
    ma.init_app(app)

    return app