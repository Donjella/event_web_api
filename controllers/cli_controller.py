from flask import Blueprint
from init import db
from models.organiser import Organiser
from models.venue import Venue
from models.event import Event  # Import Event model

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
            street_address="1 Convention Centre Pl",
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

    events = [
        Event(
            name="Tech Conference 2024",
            description="A conference for tech enthusiasts.",
            date="2024-12-01",
            time="09:00:00",
            organiser_id=1,  # Assuming Alice's organiser_id is 1
            venue_id=1       # Assuming Hilton Sydney's venue_id is 1
        ),
        Event(
            name="AI Summit 2024",
            description="Exploring the latest in AI advancements.",
            date="2025-01-15",
            time="10:00:00",
            organiser_id=2,  # Assuming Graham's organiser_id is 2
            venue_id=2       # Assuming Melbourne Convention Centre's venue_id is 2
        ),
        Event(
            name="Developer Conference 2024",
            description="An event for software developers to network.",
            date="2024-11-20",
            time="14:00:00",
            organiser_id=3,  # Assuming Charlie's organiser_id is 3
            venue_id=3       # Assuming Brisbane Airport Conference Centre's venue_id is 3
        )
    ]
    db.session.add_all(events)

    db.session.commit()
    print("All tables seeded")
