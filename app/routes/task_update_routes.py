from flask import Flask, render_template, request, redirect, url_for, flash, session
from app.models.task_update import get_employee_tasks, update_task_status

def register_task_update_routes(app: Flask):
    @app.route('/task_update', methods=['GET', 'POST'])
    def task_update():
        user = session.get("user")
        if not user:
            return redirect("/login")
        emp_id = user.get("id")
        print(f"[DEBUG] User session data: {user}")
        print(f"[DEBUG] Using emp_id: {emp_id}")

        if request.method == 'POST':
            task_id = request.form.get('task_id')
            status_percentage = request.form.get('status_percentage')  # get the slider value

            if task_id and status_percentage is not None:
                try:
                    status_percentage = int(status_percentage)
                    # Map percentage to enum
                    if status_percentage == 100:
                        status = 'COMPLETED'
                    else:
                        status = 'PENDING'

                    update_task_status(task_id, status)
                    flash("Task status updated successfully!", "success")
                    return redirect(url_for('task_update'))
                except ValueError:
                    flash("Invalid status value.", "warning")
            else:
                flash("Please select both Task and Status.", "warning")

        tasks = get_employee_tasks(emp_id)
        print(f"[DEBUG] Tasks fetched for emp_id={emp_id}: {tasks}")
        return render_template('employee/task_update.html', tasks=tasks, user=user)
