import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os


load_dotenv()


def get_db_connection():
    try:
        
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        print("connection suxcesdjd",connection)
        
        if connection.is_connected():
            return connection
        else:
            print("Failed to connect to the database.")
            return None
    except Error as e:

        print(f"Database connection error: {e}")

        return None

