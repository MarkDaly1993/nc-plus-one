import os 
from dotenv import load_dotenv
import psycopg2


def get_connection_to_database():
    load_dotenv()

    connection = psycopg2.connect(
        dbname= os.getenv("dbname"),
        user= os.getenv("user"),
        password= os.getenv("password"),
        host= os.getenv("host"),
        port= os.getenv('port')
    )
    return connection