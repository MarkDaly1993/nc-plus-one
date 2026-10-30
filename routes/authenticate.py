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

#takes a body with email and password
#uses the User_Login
@authenticate_router.post("/login")
def authenticate_user(body: User_Login) -> dict:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE email = %s",(body.email,))
    user = cursor.fetchone()
    cursor.close()
    connection.close()
    #Checking to see if user is present inside of users
    if user is None:
        raise HTTPException(status_code=401, detail={'code': '401', 'message': 'Unauthorized failed to login'})
    #verifying the token using the verify token password.
    #returns True if they are the same
    if verify_password(body.password, user[2]):
        #creates and returns a JWT token
        return {"token" :create_access_token(user[0])}
    else:
        raise HTTPException(status_code=401, detail={'code': '401', 'message': 'Unauthorized failed to login'})


#takes a body containing name, email, password
#uses the User_Create
@authenticate_router.post("/register", status_code= 201)
def register_user(body: User_Create) -> dict:
    connection = get_connection()
    cursor = connection.cursor()
    #test to see if email is already in users
    try:
        cursor.execute("""
        INSERT INTO users (name, email, password)
        VALUES (%s, %s, %s)
        RETURNING *
        """, (body.name, body.email, hash_password(body.password)))
    except UniqueViolation:
        raise HTTPException(status_code=409, detail={'code': '409', 'message': 'Confict Email already register'})  
    else:
        user = cursor.fetchone()
        connection.commit()
        cursor.close()
        connection.close()
        return {'user' : {'id': user[0],'name': user[3], 'email': user[1], 'created_at': user[4]}}



