import os 
from dotenv import load_dotenv
import psycopg2


def get_connection_to_database():
    load_dotenv()

    connection = psycopg2.connect(
        dbname= os.getenv("database_name"),
        user= os.getenv("user_name"),
        password= os.getenv("user_password"),
        host= os.getenv("database_host"),
        port= os.getenv('database_port')
    )

    return connection