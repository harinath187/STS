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
    def get_project_manager(project_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT CONCAT(e.firstname, ' ', COALESCE(e.lastname, '')) AS manager_name
            FROM project p
            LEFT JOIN employee e ON p.project_manager = e.id
            WHERE p.id = %s
        """, (project_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result['manager_name'] if result else None

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
    def fetch_tasks_by_name(task_name):
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
            WHERE t.task_name LIKE %s
        """, ('%' + task_name + '%',))
        tasks = cursor.fetchall()
        cursor.close()
        conn.close()
        return tasks

    @staticmethod
    def fetch_tasks_by_project_and_name(project_id, task_name):
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
            WHERE t.project_id = %s AND t.task_name LIKE %s
        """, (project_id, '%' + task_name + '%'))
        tasks = cursor.fetchall()
        cursor.close()
        conn.close()
        return tasks
