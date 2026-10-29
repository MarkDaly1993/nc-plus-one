from fastapi import APIRouter, HTTPException, Response, status
from db.test_setup_files.connection_test import get_connection_to_database_test as get_connection
from pydantic import BaseModel
from typing import Optional
from db.test_setup_files.password import hash_password, verify_password
from jwt_token import create_access_token
from psycopg2.errors import UniqueViolation



authenticate_router = APIRouter(prefix='/api/auth')

class User_Login(BaseModel):
    email: str 
    password: str

class User_Create(BaseModel):
    name: str
    email: str
    password: str

@authenticate_router.post("/login")
def authenticate_user(body: User_Login):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE email = %s",(body.email,))
    user = cursor.fetchone()
    cursor.close()
    connection.close()
    if user is None:
        raise HTTPException(status_code=401, detail={'code': '401', 'message': 'Unauthorized failed to login'})
    if verify_password(body.password, user[2]):
        return {"token" :create_access_token(user[0])}
    else:
        raise HTTPException(status_code=401, detail={'code': '401', 'message': 'Unauthorized failed to login'})

@authenticate_router.post("/register", status_code= 201)
def register_user(body: User_Create):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("""
        INSERT INTO users (name, email, password)
        VALUES (%s, %s, %s)
        RETURNING *
        """, (body.name, body.email, hash_password(body.password)))
    except UniqueViolation:
        raise HTTPException(status_code=409, detail={'code': '409', 'message': 'Unauthorized failed to login'})  
    else:
        user = cursor.fetchone()
        connection.commit()
        cursor.close()
        connection.close()
        return {'user' : {'id': user[0],'name': user[3], 'email': user[1], 'created_at': user[4] }}


# @app.post("/missions", status_code=201)
# def create_mission(mission: MissionCreate):
#     conn = get_connection()
#     cursor = conn.cursor()
#     cursor.execute("""
#     INSERT INTO missions (name, destination, status, spacecraft_id)
#     VALUES (%s, %s, %s, %s)
#     RETURNING *
#     """, (mission.name, mission.destination, mission.status, mission.spacecraft_id))
#     columns = [desc[0] for desc in cursor.description]
#     row = cursor.fetchone()
#     conn.commit()
#     cursor.close()
#     conn.close()
#     return dict(zip(columns, row))
