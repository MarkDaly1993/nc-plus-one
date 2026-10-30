REST API for an events platform.

This API will allow users to 

register as a new user,
browse events by id,
Create a RSVP for an event as well as cancel that RSVP,


Orignisers will be able to 

Create events
mange events
view statistics about audiences.


DIRCTORIES

db - Contains the setup files for both the production and test data bases. The are split into two dirctories one called production
the other called test_setup_files. It includes the files to create the database (setup.sql), the file to create and populate the tables(seed.py), a file
that connects to each data base and a folder containing the raw data in json files to populate the database. 

routes - This contains the the files storing the different function for each endpoint. Each one has a APIRouter that connects to the app which is
the FastAPI connection in main.py.

tests - is a directory that contains all the tests for each endpoint. They run using pytest and each one has a pytest fixture that reseeds the test_database
when a test is run.

In the route directory there are a couple of files of note firstly the main.py which houses the FastAPI connection. Each file from route has a APIRoute that main
imports and includes into the connection. There is also a exception handler that returns a status code of 400 for validation errors. This happens when you try
to run an endpoint but the information given is malformed or the wrong type.

The jwt.token is a file houses functions for the creation, decodeing and validation of JWT tokens. Sevral endpoints within this API are designed to
only run if a JWT token is given and it can be validated.


SETUP

- Create a virtial enviviroment in your terminal.

python -m venv venv

- to activate it 

source venv/bin/activate

- install the requirments from with in the requierments.txt file.

pip install -r requirements.txt

this will give install the trird party models such as fastapi, unicorn, pytest and bycript

- create a new database in your temrminal. If you are using both the test data base and 
the proction one you will need to create two.

the db dirctory is split into one for a production database the other for a test one.
to create one of each run the sql file within the specific folder. You can also use this to 
reset the database but beaware all tables and contents will be erased. 
Do so at your own caution.

- two seed the database you will first have to set up the enviroment varriables. 

You will find an example for what the varriables are needed. 
If you are creating more than one datatbase you will require a .env files for the each one.
below is the contents of the .env.example

dbname=''
user=''
password=''
host=''
port=5432
JWT_SECRET= ''

the first 5 are required for the connecting to the database the JWT_SECRET is required for 
the creation of and to decode JWT tokens used for authorisation

- each folder contains a connection file that has a function used to connect to the specified database.

change the load_dotenv() to refence you specific .env file.

- in in db folder there is a seed file run this file to create the specific tables the enter the data contained within the 
data folder's json files into the corisponding database tables. 

If the seed is ran again it will reset the database and any changes that have been made will be losted.

- to Run the server in a terminal enter. 

uvicorn main:app --reload

DATABASE

- tables -
    events,  
    rsvps,  
    users, 
    venues

- events coloumes -
    id, 
    title,  
    description, 
    starts_at, 
    ends_at, 
    organiser_id, 
    venue_id, 
    created_at

- rsvps coloums
    id, 
    attendee_id, 
    event_id, 
    created_at

- users coloums
    id, 
    email, 
    password, 
    name, 
    created_at, 

- venues coloums
    id, 
    name, 
    address, 
    capacity


ENDPOINTS

- GET /api/events
inside events.py
function name - get_events()

returns a dictionary with the value being a list of dictionary repersenting the every event from the events table.

- GET /api/events/{id}
inside events.py
function name - get_event()

returns a dictonary with the single event in a dictonary as its value. Requires a valid id to work.

- POST /api/auth/login
inside authenticate.py
function name - authenticate_user()

takes a json body containing an email and a password written in plain text. 
The function then test to see if both the email and password are contained in the users
table in the database. if so it returns a JWT token in a dictonary and creates a new user
in the user table.


- POST /api/auth/register
inside authenticate.py
function name - register_user()

takes a json body with a name, email and password whcih is written in plain text.
The function check to see if the email is already present in users.
if so it sends back an status code of 409.
if not it creates a new user in the users table and returns the new entry as a dictonary.

- POST /api/events/{id}/rsvp
inside events.py
function name - create_rsvp()

takes a header containing a Bearer and valid JWT token.
The function firstly validates the token if its invalid it returns a status code 
of 401.
if the token is valid and that the event exists it creates a new rsvp.
it returns this entry as a dictonary.

- DELETE /api/events/{id}/rsvp/me

inside events.py
function name - delete_rsvp()

takes a header containing a Bearer and valid JWT token.
The fuction firstly validates the token if its invalid it returns a status
code of 401.
if the token is vaild it checks to see if there is a rsvp if not it sends
back a 404. if so it then deletes that rsvp.
