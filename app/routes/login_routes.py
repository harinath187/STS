
from flask import render_template, request, redirect, session
from app.models.db import get_db_connection

from app.models.login import get_user_by_credentials  





def register_routes(app):

    @app.route("/")
    @app.route("/login", methods=["GET"])
    def login_page():
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
        elif role =="IT Project Manager":
            return redirect("/it_manager")
        else:
            return render_template("auth/login.html", error="Unknown role")

    @app.route("/admin")
    def admin_dashboard():
        user = session.get("user")
        if not user:
            return redirect("/login")
        return render_template("dashboard/admin.html",user=user)

    @app.route("/employee_home")
    def employee_home():
        user = session.get("user")
        if not user:
            return redirect("/login")
        return render_template("dashboard/employee.html",user=user)
    


    @app.route("/manager")
    def manager_dashboard():
        user = session.get("user")
        if not user:
            return redirect("/login")
        return render_template("dashboard/pm.html",user=user)

    @app.route("/it_employee")
    def it_employee_dashboard():
        user = session.get("user")
        if not user:
            return redirect("/login")
        return render_template("dashboard/it_emp.html",user=user)
    # @app.route("/it_manager")
    # def it_manager():
    #     user = session.get("user")
    #     if not user:
    #         return redirect("/login")
    #     return render_template("dashboard/it_manager.html",user=user)
    @app.route("/logout")
    def logout():
        return render_template("auth/login.html")
    @app.context_processor
    def inject_user():
        return dict(user=session.get("user"))