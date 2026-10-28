from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
import jwt
import os

ALGOTITHEM = "HS256"


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