# /app/models/employee/mytickets.py
from app.models.db import get_db_connection

def get_tasks_by_employee(emp_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
    SELECT
        pt.task_id,
        pt.task_name,
        pt.task_description,
        pt.task_Duration,
        pt.project_id,
        pt.assigned_to,
        pt.assigned_by,
        pt.estimated_hrs,
        pt.worked_hrs,
        pt.Start_Date,
        pt.End_Date,
        pt.Comments,
        pt.status,
        p.project_name,
        e.firstname AS assigned_to_firstname,
        e.lastname AS assigned_to_lastname,
        emp.firstname AS assigned_by_firstname,
        emp.lastname AS assigned_by_lastname
    FROM
        project_task pt
    JOIN
        project p ON pt.project_id = p.id
    JOIN
        employee e ON pt.assigned_to = e.id
    JOIN
        employee emp ON pt.assigned_by = emp.id
    WHERE
        pt.assigned_to = %s;
    """

    cursor.execute(query, (emp_id,))
    tasks = cursor.fetchall()
    
    cursor.close()
    connection.close()

    return tasks
