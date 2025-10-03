from app.models.db import get_db_connection
from datetime import datetime

# Total tasks assigned to employee
def get_total_tasks(emp_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM project_task WHERE assigned_to = %s", (emp_id,))
    total = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return total

# Pending tasks
def get_pending_tasks(emp_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM project_task WHERE assigned_to = %s AND status='PENDING'", (emp_id,))
    pending = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return pending

# Completed tasks
def get_completed_tasks(emp_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM project_task WHERE assigned_to = %s AND status='COMPLETED'", (emp_id,))
    completed = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return completed

# Support tickets raised by employee
def get_support_tickets(emp_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM support_ticket WHERE assigned_by = %s", (emp_id,))
    tickets = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return tickets

# Recent tasks assigned
def get_recent_tasks(emp_id, limit=5):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT pt.task_name, pt.status, pt.Start_Date, pt.End_Date, p.project_name
        FROM project_task pt
        JOIN project p ON pt.project_id = p.id
        WHERE pt.assigned_to = %s
        ORDER BY pt.created_at DESC
        LIMIT %s
    """, (emp_id, limit))
    tasks = cursor.fetchall()
    cursor.close()
    conn.close()
    return tasks

# Monthly completed tasks for line chart
def get_monthly_completed_tasks(emp_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DATE_FORMAT(End_Date, '%%Y-%%m') AS month, COUNT(*) 
        FROM project_task 
        WHERE assigned_to = %s AND status='COMPLETED'
        GROUP BY month
        ORDER BY month
    """, (emp_id,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    months = [row[0] for row in rows]
    counts = [row[1] for row in rows]
    return months, counts
def get_overdue_tasks(emp_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT * 
        FROM project_task 
        WHERE assigned_to = %s 
          AND status='PENDING' 
          AND End_Date < CURDATE()
    """, (emp_id,))
    tasks = cursor.fetchall()
    cursor.close()
    conn.close()
    return tasks

def get_all_departments():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT dept_id, dept_name FROM department ORDER BY dept_name")
    departments = cursor.fetchall()
    cursor.close()
    conn.close()
    return departments
