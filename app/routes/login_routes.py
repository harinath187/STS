from flask import render_template, request, redirect, session, url_for
from datetime import timedelta
from app.models.db import get_db_connection
from app.models.login import get_user_by_credentials


def register_routes(app):
    # Session will expire after 15 minutes of inactivity
    app.permanent_session_lifetime = timedelta(minutes=15)

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
        session.permanent = True  # This enables timeout
        session["user"] = user

        # Redirect based on role
        role = user["dep_name"].strip()

        if role == "Admin":
            return redirect("/admin")
        elif role in ["HR", "Backend Team", "Frontend Team", "QA / Testing", "Database / Data", "Security"]:
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
        if not user:
            return redirect("/login")
        return render_template("dashboard/admin.html", user=user)

    @app.route("/employee_home")
    def employee_home():
        user = session.get("user")
        if not user:
            return redirect("/login")
        return render_template("dashboard/employee.html", user=user)

    @app.route("/today_task")
    def get_new():
        from app.models.task_model import get_today_task  # Ensure you import this if needed
        today_task = get_today_task()
        return render_template("project_management/due_today.html", today_task=today_task)
