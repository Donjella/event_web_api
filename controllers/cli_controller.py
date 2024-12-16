from flask import Blueprint
from init import db
from models.organiser import Organiser
from models.venue import Venue

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

    venues = [
        Venue(
            name="Hilton Sydney",
            street_address="488 George St",
            city="Sydney",
            state="NSW",
            postcode="2000",
            capacity=500
        ),
        Venue(
            name="Melbourne Convention Centre",
            street_address="1 Convention Centre PL",
            city="Melbourne",
            state="VIC",
            postcode="3000",
            capacity=300
        ),
        Venue(
            name="Brisbane Airport Conference Centre",
            street_address="2 Dryandra Rd",
            city="Brisbane",
            state="QLD",
            postcode="4008",
            capacity=1000
        )
    ]
    db.session.add_all(venues)
    
    db.session.commit()
    print("Tables seeded")
  