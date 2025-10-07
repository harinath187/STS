# app/models/project_task_dashboard.py
from app.models.db import get_db_connection

class ProjectTaskDashboard:
    
    @staticmethod
    def get_dashboard_stats():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT COUNT(*) as total FROM project")
        total_projects = cursor.fetchone()['total']
        
        cursor.execute("SELECT COUNT(*) as total FROM project_task")
        total_tasks = cursor.fetchone()['total']
        
        cursor.execute("SELECT COUNT(*) as total FROM project_task WHERE status='COMPLETED'")
        completed_tasks = cursor.fetchone()['total']
        
        cursor.execute("SELECT COUNT(*) as total FROM project_task WHERE status='PENDING'")
        pending_tasks = cursor.fetchone()['total']
        
        cursor.execute("SELECT COUNT(*) as total FROM project WHERE status_percentage < 100")
        active_projects = cursor.fetchone()['total']
        
        cursor.close()
        conn.close()
        
        return {
            'total_projects': total_projects,
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'pending_tasks': pending_tasks,
            'active_projects': active_projects
        }
    
    @staticmethod
    def get_recent_tasks(limit=6):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT t.*, 
                   p.project_name,
                   CONCAT(e.firstname, ' ', COALESCE(e.lastname, '')) AS employee_name
            FROM project_task t
            LEFT JOIN project p ON t.project_id = p.id
            LEFT JOIN employee e ON t.assigned_to = e.id
            ORDER BY t.created_at DESC
            LIMIT %s
        """, (limit,))
        tasks = cursor.fetchall()
        cursor.close()
        conn.close()
        return tasks
    
    @staticmethod
    def get_task_status_counts():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT status, COUNT(*) as count 
            FROM project_task 
            GROUP BY status
        """)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results
    
    @staticmethod
    def get_monthly_task_counts():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT DATE_FORMAT(created_at, '%%Y-%%m') as month, COUNT(*) as count
            FROM project_task
            GROUP BY DATE_FORMAT(created_at, '%%Y-%%m')
            ORDER BY month DESC
            LIMIT 6
        """)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results