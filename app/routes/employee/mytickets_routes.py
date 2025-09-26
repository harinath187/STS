# /app/routes/employee/mytickets_routes.py
from flask import render_template
from STS.app.models.mytickets import get_tasks_by_employee

def show_my_tasks(emp_id):
    tasks = get_tasks_by_employee(emp_id)
    return render_template('employee/mytickets.html', tasks=tasks)
