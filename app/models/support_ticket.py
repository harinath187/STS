import mysql.connector
from datetime import datetime
from app.models.db import get_db_connection 

def create_support_ticket(dept_id,comments, problem_description, priority):
    """Insert a new support ticket into the database"""
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO support_ticket 
        (dept_id,comments, problem_description, Priority)
        VALUES (%s, %s, %s, %s)
    """, (dept_id,comments, problem_description, priority))

    connection.commit()
    cursor.close()
    connection.close()
