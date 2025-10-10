from app.models.db import get_db_connection
from datetime import datetime
import os

# Folder to save attachments
UPLOAD_FOLDER = "app/static/uploads/support_attachment"

def create_support_ticket(dept_id, comments, problem_description, priority, attachment_path, created_by):
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO support_ticket (dept_id, comments, problem_description, Priority, Attachment, status, created_by)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    cursor.execute(query, (
        dept_id,
        comments,
        problem_description,
        priority,
        attachment_path,
        'OPEN',         # Default status on creation
        created_by      #  New field
    ))

    connection.commit()
    cursor.close()
    connection.close()


