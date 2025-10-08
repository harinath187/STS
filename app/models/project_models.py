from app.models.db import get_db_connection

def fetch_all_projects():
    conn = get_db_connection()
    if not conn:
        return []

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM project")
        projects = cursor.fetchall()
        return projects
    except Exception as e:
        print(" Error fetching projects:", e)
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


def get_employees_assigned_by(manager_id):
    conn=get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
SELECT DISTINCT
    e.id,
    e.firstname,
    e.lastname,
    e.email,
    e.dept_id,
    r.role_name,
    d.dept_name
FROM project_task pt
JOIN employee e ON pt.assigned_to = e.id
LEFT JOIN roles r ON e.role_id = r.id
left join department d on e.dept_id=d.dept_id
WHERE pt.assigned_by = %s
ORDER BY e.firstname;
    """
    cursor.execute(query, (manager_id,))
    return cursor.fetchall()
 
