from flask import Blueprint
from init import db
from models.organiser import Organiser
from models.event import Event

db_commands = Blueprint("db", __name__)

@db_commands.cli.command("create")
def create_tables():
    db.create_all()
    print("Tables created")

@db_commands.cli.command("drop")
def drop_tables():
    db.drop_all()
    print("Tables dropped")

@db_commands.cli.command("seed")
def seed_tables():
    organisers = [
        Organiser(
            first_name="Alice",
            last_name="Johnson",
            company_name="Event Masters",
            email="alice.johnson@eventmasters.com",
            phone="0403123456"
        ),
        Organiser(
            first_name="Graham",
            last_name="Hansen",
            company_name="Super Events",
            email="graham.hansen@superevents.com",
            phone="0401123456"
        ),
        Organiser(
            first_name="Charlie",
            last_name="Brown",
            company_name="Mega Events",
            email="charlie.brown@megaevents.com",
            phone="0401223456"
        )
    ]

    db.session.add_all(organisers)
    db.session.commit()
    print("Tables seeded")
  