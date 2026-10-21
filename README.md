REST API for an events platform.

The API will allow users to 

register,
browse events,
RSVP,
Manage their attendance.

Orignisers will be able to 

Create events
mange events
view statistics about audiences.

db/setup.sql

This file exist to both create the inital nc_plus_one database as well as to delete and reset the database to an empty database (eg: no tables or contents). Be caerful doing so as all entrys within will be deleted.

connection.py

the file contains the function called get_connection_to_database() which uses enviroment varriables to contaied within a .env file for make the connection. An example of the file called .env.example is included in this repo with the required fields to give you some idea of what the connection is looking for. The function makes use of python-dotenv the version of which is stated in the requirement.txt file in this repo.