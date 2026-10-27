from fastapi import APIRouter, HTTPException
from db.test_setup_files.connection_test import get_connection_to_database_test as get_connection
from pydantic import BaseModel
from typing import Optional


event_router = APIRouter(prefix='/api/events')

@event_router.get("/")
def get_events():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM events;")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return {"events": rows}


# @app.get("/api/events")
# def get_events():
#     connection = get_connection()
#     cursor = connection.cursor()
#     cursor.execute("SELECT * FROM events;")
#     rows = cursor.fetchall()
#     cursor.close()
#     connection.close()
#     return {"events": rows}

