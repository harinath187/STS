import mysql.connector
from datetime import datetime
from app.models.db import get_db_connection 

def create_support_ticket(assigned_to, assigned_by, dept_id, duration, comments, problem_description, priority, start_date, end_date):
    """Insert a new support ticket into the database"""
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO support_ticket 
        (assigned_to, assigned_by, dept_id, duration, comments, problem_description, Priority, Start_Date, End_Date)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (assigned_to, assigned_by, dept_id, duration, comments, problem_description, priority, start_date, end_date))

    connection.commit()
    cursor.close()
    connection.close()
