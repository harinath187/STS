# app/routes/manager_routes.py

from flask import Blueprint, render_template, redirect, session
from app.models.db import get_db_connection

manager_bp = Blueprint("manager", __name__, url_prefix="/manager")

@manager_bp.route("/")
def manager_dashboard():
    user = session.get("user")
    if not user:
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM project WHERE project_lead = %s
    """, (user['id'],))
    projects = cursor.fetchall()

    in_progress_count = 0
    task_count = 0
    unassigned_task_count = 0

    if projects:
        project_ids = [p['id'] for p in projects]
        format_strings = ','.join(['%s'] * len(project_ids))

        cursor.execute(f"""
            SELECT status, emp_id 
            FROM project_ticket 
            WHERE project_id IN ({format_strings})
        """, tuple(project_ids))

        tasks = cursor.fetchall()
        task_count = len(tasks)
        in_progress_count = sum(1 for t in tasks if t['status'] == 'In Progress')
        unassigned_task_count = sum(1 for t in tasks if t['emp_id'] is None)

    cursor.close()
    conn.close()

    return render_template(
        "dashboard/pm.html",
        user=user,
        projects=projects,
        in_progress_count=in_progress_count,
        task_count=task_count,
        unassigned_task_count=unassigned_task_count
    )

@manager_bp.route("/project/<int:project_id>/tasks")
def manager_project_tasks(project_id):
    user = session.get("user")
    if not user:
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM project 
        WHERE id = %s AND project_lead = %s
    """, (project_id, user['id']))
    project = cursor.fetchone()

    if not project:
        return "Unauthorized access or project not found", 404

    cursor.execute("""
        SELECT 
            pt.token_id, pt.description, pt.estimated_hrs, pt.worked_hrs, pt.status,
            e.firstname, e.lastname, d.dept_name
        FROM project_ticket pt
        LEFT JOIN employee e ON pt.emp_id = e.id
        LEFT JOIN department d ON e.dept_id = d.dept_id
        WHERE pt.project_id = %s
    """, (project_id,))
    tasks = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("dashboard/pm_project_tasks.html", user=user, project=project, tasks=tasks)
