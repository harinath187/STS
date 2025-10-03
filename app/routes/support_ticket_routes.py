from flask import Flask, render_template, request
from datetime import datetime
from app.models.support_ticket import create_support_ticket

def register_support_ticket_routes(app: Flask):

    @app.route('/create_support_ticket', methods=['GET', 'POST'])
    def create_ticket():
        if request.method == 'POST':
            assigned_to = request.form['assigned_to']
            assigned_by = request.form['assigned_by']
            dept_id = request.form['dept_id']
            duration = request.form['duration']
            comments = request.form['comments']
            problem_description = request.form['problem_description']
            priority = request.form['priority']

            # Convert dates
            start_date = datetime.strptime(request.form['start_date'], "%Y-%m-%d")
            end_date = datetime.strptime(request.form['end_date'], "%Y-%m-%d")

            # Call model function
            create_support_ticket(
                assigned_to, assigned_by, dept_id, duration, comments,
                problem_description, priority, start_date, end_date
            )

        return render_template('employee/create_support_ticket.html')
