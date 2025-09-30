from flask import Flask, render_template, request, redirect, url_for, flash
from app.models.support_ticket import create_support_ticket
from app.models.emp_dashboard import get_all_departments  # assumes raw SQL version

def register_support_ticket_routes(app: Flask):

    @app.route('/create_support_ticket', methods=['GET', 'POST'])
    def create_ticket():
        if request.method == 'POST':
            dept_id = request.form['dept_id']
            comments = request.form['comments']
            problem_description = request.form['problem_description']
            priority = request.form['priority']

            create_support_ticket(dept_id, comments, problem_description, priority)

            flash("✅ Support ticket created successfully!", "success")
            return redirect(url_for('test_routes.test_tasks'))  # 👈 Redirect after POST

        departments = get_all_departments()
        return render_template('employee/create_support_ticket.html', departments=departments)
