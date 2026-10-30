from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import HTTPException, Depends
import jwt
import os

ALGOTITHEM = "HS256"

bearer_scheme = HTTPBearer(auto_error=False)




def get_secret():
    load_dotenv('.env.test')
    secret = os.getenv("JWT_SECRET")
    return secret

def create_access_token(id: int):
    payload = {
        "sub" : str(id),
        "exp" : datetime.now(timezone.utc) + timedelta(hours=1)
    }
    return jwt.encode(payload, get_secret(), algorithm=ALGOTITHEM)

def decode_token(token: str):
    token= token.encode()
    decoded_token = jwt.decode(token, get_secret(), algorithms=["HS256"])
    return decoded_token

def get_current_user(credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme)):

    unauthorised = HTTPException(
        status_code= 401,
        detail="Not authenticated",
        headers= {"WWW-Authenticate" : "Bearer"},
    )

    if credentials is None:
        raise unauthorised

    try:
        payload = jwt.decode(credentials.credentials, get_secret(), "HS256")
        yield payload
    except():
        raise unauthorised

    
# def check_validation_of_token()


#print(create_access_token(1))

# HTTPAuthorizationCredentials is a Pydantic data model in FastAPI 
# (fastapi.security.HTTPAuthorizationCredentials) that represents the parsed contents 
# of an HTTP Authorization header.