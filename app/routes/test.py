from flask import Blueprint, render_template, session, redirect
from app.models.test import get_tasks_by_employee

test_routes = Blueprint('test_routes', __name__)

@test_routes.route("/test")
def test_tasks():
    user = session.get("user")
    if not user:
        return redirect("/login")  # redirect if not logged in

    emp_id = user["id"]  # hardcoded from session
    tasks = get_tasks_by_employee(emp_id)
    return render_template("employee/test.html", user=user, tasks=tasks)
