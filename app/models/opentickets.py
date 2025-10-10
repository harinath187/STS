# File: app/models/opentickets.py

from app.models.db import get_db_connection  # Import this

def get_support_tickets_by_employee(emp_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
    SELECT 
        st.id,
        st.dept_id,
        st.duration,
        st.comments,
        st.problem_description,
        st.Priority,
        st.Attachment,
        st.status
    FROM support_ticket st
    WHERE st.created_by = %s;
    """
    cursor.execute(query, (emp_id,))
    tickets = cursor.fetchall()
    cursor.close()
    connection.close()
    return tickets
