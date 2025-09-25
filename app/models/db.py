
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
        return connection
    except Error as e:
        print("❌ Database Connection Error:", e)
        return None

if __name__ == "__main__":
    conn = get_db_connection()
    if conn and conn.is_connected():
        print(" Database connected successfully!")
        conn.close()
    else:
        print(" Failed to connect to the database.")
