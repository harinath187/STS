from app.models.db import get_db_connection

def get_employee_tasks(emp_id):
    """
    Fetch all tasks assigned to a specific employee.
    Returns a list of dictionaries with keys: task_id, task_name, status
    """
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    query = """
        SELECT 
            task_id, 
            task_name, 
            status 
        FROM 
            project_task 
        WHERE 
            assigned_to = %s
    """
    cur.execute(query, (emp_id,))
    tasks = cur.fetchall()

    cur.close()
    conn.close()

    # Debug print - remove or comment out in production
    print(f"[DEBUG] Tasks fetched for emp_id={emp_id}: {tasks}")

    return tasks


def update_task_status(task_id, status):
    """
    Update the status of a task given its task_id.
    """
    conn = get_db_connection()
    cur = conn.cursor()

    query = """
        UPDATE project_task
        SET status = %s
        WHERE task_id = %s
    """
    cur.execute(query, (status, task_id))
    conn.commit()

    # Debug print - remove or comment out in production
    print(f"[DEBUG] Updated task_id={task_id} with status={status}")

    cur.close()
    conn.close()
