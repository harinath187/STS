from app.models.db import get_db_connection

def get_total_projects(manager_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM project WHERE project_manager = %s", (manager_id,))
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return count

def get_total_tasks(manager_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*) FROM project_task
        WHERE project_id IN (SELECT id FROM project WHERE project_manager = %s)
    """, (manager_id,))
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return count

def get_completed_tasks(manager_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*) FROM project_task
        WHERE status = 'COMPLETED' AND project_id IN (
            SELECT id FROM project WHERE project_manager = %s
        )
    """, (manager_id,))
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return count

def get_in_progress_tasks(manager_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*) FROM project_task
        WHERE status = 'PENDING' AND project_id IN (
            SELECT id FROM project WHERE project_manager = %s
        )
    """, (manager_id,))
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return count

def get_unassigned_tasks(manager_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*) FROM project_task
        WHERE assigned_to IS NULL AND project_id IN (
            SELECT id FROM project WHERE project_manager = %s
        )
    """, (manager_id,))
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return count

def get_monthly_task_counts(manager_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DATE_FORMAT(created_at, '%%Y-%%m') AS month, COUNT(*) 
        FROM project_task
        WHERE project_id IN (
            SELECT id FROM project WHERE project_manager = %s
        )
        GROUP BY month
        ORDER BY month
    """, (manager_id,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    months = [row[0] for row in rows]
    counts = [row[1] for row in rows]
    return months, counts

def get_recent_tasks(manager_id, limit=6):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            pt.task_name, 
            pt.status, 
            pt.Start_Date, 
            pt.End_Date, 
            p.project_name
        FROM project_task pt
        JOIN project p ON pt.project_id = p.id
        WHERE p.project_manager = %s
        ORDER BY pt.created_at DESC
        LIMIT %s
    """, (manager_id, limit))
    tasks = cursor.fetchall()
    cursor.close()
    conn.close()
    return tasks
