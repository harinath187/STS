from flask import render_template, request, redirect, session
from app.models.db import get_db_connection

def register_routes(app):

    @app.route("/")
    @app.route("/login", methods=["GET"])
    def login_page():
        # print("connection success.....................")
        return render_template("auth/login.html")  

    @app.route("/login", methods=["POST"])
    def login():
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT employee.*, department.dept_name as dep_name 
            FROM employee 
            JOIN department ON employee.dept_id = department.dept_id 
            WHERE employee.username = %s AND employee.password = %s
        """, (username, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if not user:
            return render_template("auth/login.html", error="Invalid credentials")

        session["user"] = user
        role = user["dep_name"].strip()

        if role == "Admin":
            return redirect("/admin")
        elif role in ["HR", "Backend Team", "Frontend Team", "QA / Testing", "Database / Data", "Security"]:
            return redirect("/employee")
        elif role == "Project Manager":
            return redirect("/manager")
        elif role in ["IT Team", "Support / IT Helpdesk"]:
            return redirect("/it_employee")
        else:
            return render_template("auth/login.html", error="Unknown role")

    @app.route("/admin")
    def admin_dashboard():
        user = session.get("user")
        if not user:
            return redirect("/login")
        return render_template("dashboard/admin.html", user=user)

    @app.route("/employee")
    def employee_dashboard():
        user = session.get("user")
        if not user:
            return redirect("/login")
        return render_template("dashboard/employee.html", user=user)

    # @app.route("/manager")
    # def manager_dashboard():
    #     user = session.get("user")
    #     if not user:
    #         return redirect("/login")

    #     conn = get_db_connection()
    #     cursor = conn.cursor(dictionary=True)

    #     # Get all projects for this manager
    #     cursor.execute("""
    #         SELECT * 
    #         FROM project 
    #         WHERE project_lead = %s
    #     """, (user['id'],))
    #     projects = cursor.fetchall()

    #     # If no projects, counts are zero
    #     in_progress_count = 0
    #     task_count = 0
    #     unassigned_task_count = 0

    #     if projects:
    #         project_ids = [p['id'] for p in projects]
    #         format_strings = ','.join(['%s'] * len(project_ids))

            
    #         cursor.execute(f"""
    #             SELECT status, emp_id 
    #             FROM project_ticket 
    #             WHERE project_id IN ({format_strings})
    #         """, tuple(project_ids))

    #         tasks = cursor.fetchall()
    #         task_count = len(tasks)
    #         in_progress_count = sum(1 for t in tasks if t['status'] == 'In Progress')
    #         unassigned_task_count = sum(1 for t in tasks if t['emp_id'] is None)

    #     cursor.close()
    #     conn.close()

    #     return render_template(
    #         "dashboard/pm.html",
    #         user=user,
    #         projects=projects,
    #         in_progress_count=in_progress_count,
    #         task_count=task_count,
    #         unassigned_task_count=unassigned_task_count
    #     )

    # @app.route("/manager/project/<int:project_id>/tasks")
    # def manager_project_tasks(project_id):
    #     user = session.get("user")
    #     if not user:
    #         return redirect("/login")

    #     conn = get_db_connection()
    #     cursor = conn.cursor(dictionary=True)

        
    #     cursor.execute("""
    #         SELECT * FROM project 
    #         WHERE id = %s AND project_lead = %s
    #     """, (project_id, user['id']))
    #     project = cursor.fetchone()

    #     if not project:
    #         return "Unauthorized access or project not found", 404

       
    #     cursor.execute("""
    #         SELECT 
    #             pt.token_id, pt.description, pt.estimated_hrs, pt.worked_hrs, pt.status,
    #             e.firstname, e.lastname, d.dept_name
    #         FROM project_ticket pt
    #         LEFT JOIN employee e ON pt.emp_id = e.id
    #         LEFT JOIN department d ON e.dept_id = d.dept_id
    #         WHERE pt.project_id = %s
    #     """, (project_id,))
    #     tasks = cursor.fetchall()

    #     cursor.close()
    #     conn.close()

    #     return render_template("dashboard/pm_project_tasks.html", user=user, project=project, tasks=tasks)

    # @app.route("/it_employee")
    # def it_employee_dashboard():
    #     user = session.get("user")
    #     if not user:
    #         return redirect("/login")
    #     return render_template("dashboard/it_emp.html", user=user)

    # @app.route("/logout")
    # def logout():
    #     session.clear()
    #     return redirect("/login")
