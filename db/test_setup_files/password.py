import os
import bcrypt


def hash_password(password: str):
    """Creates a hashed version of a given password
    uses bycrypt.gensalt to allow two of the same password 
    and for the token to still be unique.
    the number of rounds can be in increased the salt and make the password 
    harder to identify."""
    rounds= 4 
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds)).decode()

def verify_password(password: str, hashed_password: str) -> bool:
    """compaires a hashed password aginst a plain text on
    returns True is they are the same or False if they are not"""
    return bcrypt.checkpw(password.encode(), hashed_password.encode())