from fastapi import APIRouter, HTTPException, Response, status, Depends
from db.test_setup_files.connection_test import get_connection_to_database_test as get_connection
from pydantic import BaseModel
from typing import Optional
from jwt_token import decode_token, get_current_user
from psycopg2.errors import ForeignKeyViolation
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer



event_router = APIRouter(prefix='/api/events')

class Rsvp_Booking(BaseModel):
    token: str

# class Event_Create(BaseModel):
#     title: str
#     description: str
#     starts_at: str
#     end_at: str
#     venue_id: int


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


@event_router.post("/{event_id}/rsvp", status_code=201)
def create_rsvp(event_id: int, body: Rsvp_Booking):
    connection = get_connection()
    cursor = connection.cursor()
    decoded_token = decode_token(body.token)
    user_id = decoded_token['sub']
    cursor.execute("SELECT * FROM rsvps WHERE attendee_id = %s AND event_id = %s;", (user_id, event_id))
    rows = cursor.fetchall()
    if len(rows) != 0:
        raise HTTPException (status_code=409, detail={'code': '409', 'message': 'Conflict: you already have a booking'})
    try:  
        cursor.execute("""
        INSERT INTO rsvps (attendee_id, event_id)
        VALUES (%s, %s)
        RETURNING *
        """, (user_id, event_id))
    except ForeignKeyViolation:
        raise HTTPException (status_code=404, detail={'code': '404', 'message': 'event not found'})
    rsvp = cursor.fetchone()
    connection.commit()
    cursor.close()
    connection.close()
    return{"rsvp": {"id": rsvp[0], "attendee_id": rsvp[1], "event_id": rsvp[2], "created_at": rsvp[3]}}

@event_router.delete("/{event_id}/rsvp/me", status_code=204)
def delete_rsvp(event_id: int, body: dict = Depends(get_current_user)):
    connection = get_connection()
    cursor = connection.cursor()
    user_id = body['sub']
    cursor.execute("SELECT * FROM rsvps WHERE attendee_id = %s AND event_id = %s;", (user_id, event_id))
    row = cursor.fetchone()
    if row is None:
        raise HTTPException (status_code=404, detail={'code': '404', 'message': 'booking not found'})
    cursor.execute("DELETE FROM rsvps WHERE attendee_id = %s AND event_id = %s;", (user_id, event_id))
    connection.commit()
    cursor.close()
    connection.close()

# @event_router.post("/", status_code=204)
# def create_event(body:)


    





