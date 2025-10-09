
from flask import render_template, request, redirect, session, url_for, jsonify
from datetime import timedelta
from app.models.db import get_db_connection
from app.models.login import get_user_by_credentials

from mysql.connector import Error

from app.models.hr import employeelist,departmentlist,roleslist

 
def register_routes(app):
    
    app.permanent_session_lifetime = timedelta(days=30)
 
    @app.route("/")
    @app.route("/login", methods=["GET"])
    def login_page():
        return render_template("auth/login.html")
 
    @app.route("/login", methods=["POST"])
    def login():
        username = request.form["username"]
        password = request.form["password"]
 
        # Get user
        user = get_user_by_credentials(username, password)
 
        if not user:
            return render_template("auth/login.html", error="Invalid credentials")
 
        # Set session
        session.permanent = True
        session["user"] = user
 
        # Redirect based on role
        role = user["dep_name"].strip()
 
        if role == "HR":
            return redirect("/admin")
        elif role in ["Backend Team", "Frontend Team", "QA / Testing", "Database / Data", "Security"]:
            return redirect("/employee")
        elif role == "Project Manager":
            return redirect("/manager")
        elif role in ["IT Team", "Support / IT Helpdesk"]:
            return redirect("/it_employee")
        elif role == "IT Project Manager":
            return redirect("/it_manager")
        else:
            return render_template("auth/login.html", error="Unknown role")
 
    @app.route("/logout")
    def logout():
        session.clear()
        return redirect(url_for('login_page', timeout='1'))
 
    @app.route("/admin")
    def admin_dashboard():
        user = session.get("user")
        department=departmentlist()
        roles=roleslist()
        listitem=employeelist()
        if not user:
            return redirect("/login")
        return render_template("hr/list_of_employees.html", user=user,employeelist=listitem,dept_list=department,role=roles)
    @app.route("/employee_home")
    def employee_home():
        user = session.get("user")
        if not user:
            return redirect("/login")
        return render_template("dashboard/employee.html", user=user)
 
    @app.route("/today_task")
    def get_new():
        from app.models.task_model import get_today_task  
        today_task = get_today_task()
        return render_template("project_management/due_today.html", today_task=today_task)
 
    # ---------------- Profile Modal JSON Route ----------------
    @app.route("/profile_data")
    def profile_data():
        user = session.get("user")
        if not user:
            return {"error": "Not logged in"}, 401
 
        username = user["username"]
        conn = get_db_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT e.id, e.firstname, e.lastname, e.username, e.email, e.password, e.dept_id, e.role_id, e.created_at, e.updated_at,
                       d.dept_name
                FROM employee e
                LEFT JOIN department d ON e.dept_id = d.dept_id
                WHERE e.username = %s
            """, (username,))
            employee = cursor.fetchone()
            cursor.close()
            conn.close()
 
            if not employee:
                return {"error": "Employee not found"}, 404
 
            return employee
 
        except Error as e:
            if conn.is_connected():
                conn.close()
            return {"error": str(e)}, 500
 
    
    @app.route("/update_profile", methods=["POST"])
    def update_profile():
        user = session.get("user")
        if not user:
            return jsonify({"error": "Not logged in"}), 401
 
        data = request.get_json()
        emp_id = data.get("id")
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")  
 
       
        import re
        if len(re.findall(r'\d', password)) < 2 or len(re.findall(r'[@#]', password)) < 2:
            return jsonify({"error": "Password must contain at least 2 numbers and 2 special characters (@ or #)"}), 400
 
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE employee
                SET username=%s, email=%s, password=%s
                WHERE id=%s
            """, (username, email, password, emp_id))
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({"success": True})
        except Error as e:
            if conn.is_connected():
                conn.close()
            return jsonify({"error": str(e)}), 500
 
 