from app.models.db import get_db_connection
from flask import session
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
    user = session.get("user")
    project_manager = user["id"]
    conn = get_db_connection()
    
    # print(data.get('estimated_duration'))
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
            data['client_name'],
            project_manager,
            data.get('estimated_duration'),
            
            data.get('tech_stack'),
            data.get('time_taken'),
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

def update_project_model(project_id):
    conn = get_db_connection()
    if not conn:
        return []

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT project_id, project_name, client_id, estimated_duration, 
                tech_stack, time_taken, cost_hours, attachments, status_percentage
            FROM projects WHERE project_id = %s
            """, (project_id,))
        project = cursor.fetchone()

        
        return project
    except Exception as e:
        print(" Error fetching projects:", e)
        return []
    finally:
        cursor.close()
        conn.close()

def delete_project_by_id(project_id):
    conn = get_db_connection()
    print("project _ id ......",project_id)
    if not conn:
        return []

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("  Delete FROM project WHERE id = %s  ", (project_id,))
        print("cursor return.......",cursor)
        # print("project deleted from  the database......",project)
        conn.commit()
        
    except Exception as e:
        print(" Error fetching projects:", e)
        return []
    finally:
        cursor.close()
        conn.close()        

   