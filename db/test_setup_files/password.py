import os

import bcrypt

def hash_password(password: str):
    rounds= 4 
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds)).decode()

def verify_password(password: str, hashed_password: str):
    return bcrypt.checkpw(password.encode(), hashed_password.encode())