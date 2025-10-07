# app/models/project_task.py
from app.models.db import get_db_connection

class ProjectTask:

    @staticmethod
    def fetch_all_projects():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT p.id, p.project_name, CONCAT(e.firstname, ' ', COALESCE(e.lastname, '')) AS project_manager_name
            FROM project p
            LEFT JOIN employee e ON p.project_manager = e.id
        """)
        projects = cursor.fetchall()
        cursor.close()
        conn.close()
        return projects

    @staticmethod
    def fetch_all_employees():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, CONCAT(firstname, ' ', COALESCE(lastname, '')) AS employee_name
            FROM employee
        """)
        employees = cursor.fetchall()
        cursor.close()
        conn.close()
        return employees

    @staticmethod
    def fetch_all_tasks():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT t.*, 
                   p.project_name,
                   t.`Start_Date`,
                   t.`End_Date`,
                   CONCAT(e.firstname, ' ', COALESCE(e.lastname, '')) AS employee_name,
                   CONCAT(m.firstname, ' ', COALESCE(m.lastname, '')) AS manager_name,
                   t.Comments AS manager_comments
            FROM project_task t
            LEFT JOIN employee e ON t.assigned_to = e.id
            LEFT JOIN employee m ON t.assigned_by = m.id
            LEFT JOIN project p ON t.project_id = p.id
        """)
        tasks = cursor.fetchall()
        cursor.close()
        conn.close()
        return tasks

    @staticmethod
    def fetch_tasks_by_project(project_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT t.*, 
                   p.project_name,
                   t.`Start_Date`,
                   t.`End_Date`,
                   CONCAT(e.firstname, ' ', COALESCE(e.lastname, '')) AS employee_name,
                   CONCAT(m.firstname, ' ', COALESCE(m.lastname, '')) AS manager_name,
                   t.Comments AS manager_comments
            FROM project_task t
            LEFT JOIN employee e ON t.assigned_to = e.id
            LEFT JOIN employee m ON t.assigned_by = m.id
            LEFT JOIN project p ON t.project_id = p.id
            WHERE t.project_id = %s
        """, (project_id,))
        tasks = cursor.fetchall()
        cursor.close()
        conn.close()
        return tasks

    @staticmethod
    def add_task(project_id, task_name, task_description, task_duration, assigned_to, assigned_by, 
                 estimated_hrs, worked_hrs, start_date, end_date, comments, status):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO project_task 
            (project_id, task_name, task_description, task_Duration, assigned_to, assigned_by, 
             estimated_hrs, worked_hrs, Start_Date, End_Date, Comments, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (project_id, task_name, task_description, task_duration, assigned_to, assigned_by,
              estimated_hrs, worked_hrs, start_date, end_date, comments, status))
        task_id = cursor.lastrowid
        conn.commit()
        cursor.close()
        conn.close()
        return task_id

    @staticmethod
    def get_task_by_id(task_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT t.*, 
                   p.project_name,
                   CONCAT(e.firstname, ' ', COALESCE(e.lastname, '')) AS employee_name,
                   CONCAT(m.firstname, ' ', COALESCE(m.lastname, '')) AS manager_name
            FROM project_task t
            LEFT JOIN employee e ON t.assigned_to = e.id
            LEFT JOIN employee m ON t.assigned_by = m.id
            LEFT JOIN project p ON t.project_id = p.id
            WHERE t.task_id = %s
        """, (task_id,))
        task = cursor.fetchone()
        cursor.close()
        conn.close()
        return task

    @staticmethod
    def update_task(task_id, project_id, task_name, task_description, task_duration, assigned_to, 
                    assigned_by, estimated_hrs, worked_hrs, start_date, end_date, comments, status):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE project_task 
            SET project_id=%s, task_name=%s, task_description=%s, task_Duration=%s, 
                assigned_to=%s, assigned_by=%s, estimated_hrs=%s, worked_hrs=%s, 
                Start_Date=%s, End_Date=%s, Comments=%s, status=%s
            WHERE task_id=%s
        """, (project_id, task_name, task_description, task_duration, assigned_to, assigned_by,
              estimated_hrs, worked_hrs, start_date, end_date, comments, status, task_id))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def delete_task(task_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM project_task WHERE task_id = %s", (task_id,))
        conn.commit()
        cursor.close()
        conn.close()

    # ========== TASK_COMMENTS METHODS ==========
    
    @staticmethod
    def add_task_attachment(task_id, attachment_path, message="Attachment uploaded"):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Task_Comments (task_id, Message, Attachment)
            VALUES (%s, %s, %s)
        """, (task_id, message, attachment_path))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def get_task_attachments(task_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT Comment_id, task_id, Message, Attachment
            FROM Task_Comments
            WHERE task_id = %s AND Attachment IS NOT NULL AND Attachment != ''
            ORDER BY Comment_id DESC
        """, (task_id,))
        attachments = cursor.fetchall()
        cursor.close()
        conn.close()
        return attachments

    @staticmethod
    def get_latest_task_attachment(task_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT Attachment
            FROM Task_Comments
            WHERE task_id = %s AND Attachment IS NOT NULL AND Attachment != ''
            ORDER BY Comment_id DESC
            LIMIT 1
        """, (task_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result['Attachment'] if result else None

    @staticmethod
    def delete_task_attachment(comment_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Task_Comments WHERE Comment_id = %s", (comment_id,))
        conn.commit()
        cursor.close()
        conn.close()