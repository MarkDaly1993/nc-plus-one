import psycopg2
from connection import get_connection_to_database
import json



#connection = psycopg2.connect(
#    dbname="nc_plus_one",
#    user="postgres",
#    password="password",
#    host="localhost",
#    port=5432 
#)

def create_database_tables():
    cursor = connection.cursor()

    cursor.execute(
        """CREATE TABLE Users (
            id SERIAL PRIMARY KEY, 
            email VARCHAR(255) UNIQUE NOT NULL, 
            password VARCHAR(255) NOT NULL, 
            name VARCHAR(255) NOT NULL, 
            created_at TIMESTAMPTZ DEFAULT NOW()
        );""")

    cursor.execute(
        """CREATE TABLE Venues (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            address TEXT,
            capacity INT
        );""")

    cursor.execute(
        """CREATE TABLE Events (
            id SERIAL PRIMARY KEY, 
            title VARCHAR(255) NOT NULL, 
            description VARCHAR(255), 
            starts_at TIMESTAMPTZ NOT NULL, 
            ends_at TIMESTAMPTZ NOT NULL,
            organiser_id INT,
            CONSTRAINT fk_Users
            FOREIGN KEY (organiser_id)
            REFERENCES Users(id),
            venue_id INT,
            CONSTRAINT fk_Venues
            FOREIGN KEY (venue_id)
            REFERENCES Venues(id),
            created_at TIMESTAMPTZ DEFAULT NOW()
        );""")
        
    cursor.execute(
        """CREATE TABLE Rsvps (
            id SERIAL PRIMARY KEY,
            attendee_id INT,
            CONSTRAINT fk_Users
            FOREIGN KEY (attendee_id)
            REFERENCES Users(id),
            event_id INT,
            CONSTRAINT fk_Events
            FOREIGN KEY (event_id)
            REFERENCES Events(id)
        );""")

    cursor.close()


def drop_tables_if_they_exist():
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS Rsvps;")
    cursor.execute("DROP TABLE IF EXISTS Events;")
    cursor.execute("DROP TABLE IF EXISTS Venues;")
    cursor.execute("DROP TABLE IF EXISTS Users")
    cursor.close()

def populate_data_base_with_user_data():
    cursor = connection.cursor()
    with open("db/data/users.json") as file:
        user_data = json.load(file)
    for user in user_data:
        statment = "INSERT INTO Users (name, email, password) VALUES (%s, %s, %s);"
        cursor.execute(statment, 
        (user['name'], user['email'], user['password']))
    cursor.close()

def populate_data_base_with_venue_data():
    cursor = connection.cursor()
    with open("db/data/venues.json") as file:
        venues_data = json.load(file)
    for venue in venues_data:
        statment = "INSERT INTO Venues (name, address, capacity) VALUES (%s, %s, %s);"
        cursor.execute(statment, 
        (venue['name'], venue['address'], venue['capacity']))
    cursor.close()

def populate_data_base_with_event_data():
    cursor = connection.cursor()
    with open("db/data/events.json") as file:
        events_data = json.load(file)
    for event in events_data:
        statment = "INSERT INTO Events (title, description, starts_at, ends_at, organiser_id, venue_id) VALUES (%s, %s, %s, %s, %s, %s);"
        cursor.execute(statment, 
        (event['title'], event['description'], event['starts_at'], event['ends_at'], event['organiser_id'], event['venue_id']))
    cursor.close()

def populate_data_base_with_rsvps_data():
    cursor = connection.cursor()
    with open("db/data/rsvps.json") as file:
        rsvps_data = json.load(file)
    for rsvp in rsvps_data:
        statment = "INSERT INTO Rsvps (attendee_id, event_id) VALUES (%s, %s);"
        cursor.execute(statment, 
        (rsvp['attendee_id'], rsvp['event_id']))
    cursor.close()

def add_entrys_to_database_table(table, *args):
    cursor = connection.cursor()
    if table.lower() == 'users': 
        for entrys in args:
            statment = "INSERT INTO Users (name, email, password) VALUES (%s, %s, %s);"
            cursor.execute(statment, 
            (entrys['name'], entrys['email'], entrys['password']))
    
    if table.lower() == 'venues': 
        for entrys in args:
            statment = "INSERT INTO Venues (name, address, capacity) VALUES (%s, %s, %s);"
            cursor.execute(statment, 
            (entrys['name'], entrys['address'], entrys['capacity']))

    if table.lower() == 'events': 
        for entrys in args:
            statment = "INSERT INTO Events (title, description, starts_at, ends_at, organiser_id, venue_id) VALUES (%s, %s, %s, %s, %s, %s);"
            cursor.execute(statment, 
            (entrys['title'], entrys['description'], entrys['starts_at'], entrys['ends_at'], entrys['organiser_id'], entrys['venue_id']))

    if table.lower() == 'rsvps': 
        for entrys in args:
            statment = "INSERT INTO Rsvps (attendee_id, event_id) VALUES (%s, %s);"
            cursor.execute(statment, 
            (entrys['attendee_id'], entrys['event_id']))
    else:
        cursor.close()
        return 'Sorry you have not entered a vaild table'
    cursor.close()

def seed():
    drop_tables_if_they_exist()
    create_database_tables()
    populate_data_base_with_user_data()
    populate_data_base_with_venue_data()
    populate_data_base_with_event_data()
    populate_data_base_with_rsvps_data()


connection = get_connection_to_database()

seed()

#drop_tables_if_they_exist()
#create_database_tables()
#add_entrys_to_database_table('Users', {"name": "Alice Rahman","email": "alice@example.com","password": "password123"})
#add_entrys_to_database_table('Venues',  {"name": "Nexus, University of Leeds","address": "Discovery Way, Leeds, LS2 3AA","capacity": 200})
#add_entrys_to_database_table('Events', {"title": "Intro to Machine Learning Workshop","description": "Hands-on workshop covering perceptrons, neural networks, and classifiers using NumPy and PyTorch.","starts_at": "2026-06-25T10:00:00+01:00","ends_at": "2026-06-25T13:00:00+01:00", "organiser_id": 1,"venue_id": 1})
#add_entrys_to_database_table('Rsvps', { "attendee_id": 1, "event_id": 1 })
#populate_data_base_with_user_data()
#populate_data_base_with_venue_data()
#populate_data_base_with_event_data()
#populate_data_base_with_rsvps_data()

connection.commit()

connection.close()


