from fastapi import APIRouter, HTTPException, Response, status
from db.test_setup_files.connection_test import get_connection_to_database_test as get_connection
from pydantic import BaseModel
from typing import Optional


user_router = APIRouter()

class User_Login(BaseModel):
    email : str 
    password : str

@user_router.post("/api/auth/login")
def authenticate_user(login: User_Login):
    pass