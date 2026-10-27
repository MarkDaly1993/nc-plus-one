from fastapi import APIRouter, HTTPException, Response, status
from db.test_setup_files.connection_test import get_connection_to_database_test as get_connection
from pydantic import BaseModel
from typing import Optional


event_router = APIRouter(prefix='/api/events')

#If called will return all the entrys in events. THe body indules location from the venues table
@event_router.get("/")
def get_events():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM events RIGHT JOIN venues ON events.venue_id = venues.id;")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    rows_list = []
    for row in rows:
        rows_list.append({'id': row[0], 'title': row[1], 'start_at': row[2], 'end_at': row[3], 'location' : row[9]})
    return {"events": rows_list}

#If called will return a single event based on the id passed in. returned body also includes the locacation ,address and capacity from
@event_router.get("/{event_id}", status_code=200)
def get_event(event_id: int):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM events RIGHT JOIN venues ON events.venue_id  = venues.id WHERE events.id = %s;", (event_id,))
    if type(event_id) != int:
        raise HTTPException (status_code=400, detail={'code': '400', 'message': 'invalid ID'})
    row = cursor.fetchone()
    cursor.close()
    connection.close()
    if row is None:
        raise HTTPException (status_code=404, detail={'code': '404', 'message': 'event not found'})
    return {'event': {'id': row[0],'title': row[1], 'description' : row[2], 'starts_at': row[3], 'ends_at' : row[4], 'location': row[9], 'address': row[10],'capacity': row[11], 'created_at': row[7]}}




    # row = cursor.fetchone()
    # cursor.close()
    # connection.close()


# @app.get("/api/events")
# def get_events():
#     connection = get_connection()
#     cursor = connection.cursor()
#     cursor.execute("SELECT * FROM events;")
#     rows = cursor.fetchall()
#     cursor.close()
#     connection.close()
#     return {"events": rows}

