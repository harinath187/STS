from app.models.db import get_db_connection

def fetch_projects_by_pm(pm_id):
    conn = get_db_connection()
    if not conn:
        return []

    try:
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM project WHERE project_manager = %s"
        cursor.execute(query, (pm_id,))
        projects = cursor.fetchall()
        return projects
    except Exception as e:
        print("Error fetching projects:", e)
        return []
    finally:
        cursor.close()
        conn.close()


def insert_project(data):
    conn = get_db_connection()
    if not conn:
        return False

    try:
        cursor = conn.cursor()
        query = """
            INSERT INTO project (
                project_name, client_id, project_manager,
                estimated_duration_months, tech_stack,
                actual_time_taken, cost_hours, Attachment,
                status_percentage
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            data['project_name'],
            data['client_id'],
            data.get('project_manager'),
            data.get('estimated_duration_months'),
            data.get('tech_stack'),
            data.get('actual_time_taken'),
            data.get('cost_hours'),
            data.get('Attachment'),
            data.get('status_percentage')
        )
        cursor.execute(query, values)
        conn.commit()
        return True
    except Exception as e:
        print(" Error inserting project:", e)
        return False
    finally:
        cursor.close()
        conn.close()


def count_projects_by_pm(pm_name):
    db = get_db_connection()
    cursor = db.cursor()
    query = """
        SELECT COUNT(*)
        FROM project p
        JOIN employee e ON p.project_manager = e.id
        WHERE e.username = %s
    """
    cursor.execute(query, (pm_name,))
    result = cursor.fetchone()
    return result[0] if result else 0
