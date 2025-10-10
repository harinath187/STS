from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
import os
from app.models.support_ticket import create_support_ticket, UPLOAD_FOLDER
from app.models.emp_dashboard import get_all_departments

def register_support_ticket_routes(app: Flask):

    @app.route('/create_support_ticket', methods=['GET', 'POST'])
    def create_ticket():
        user = session.get("user")
        if not user:
            return redirect("/login")

        if request.method == 'POST':
            dept_id = request.form['dept_id']
            comments = request.form['comments']
            problem_description = request.form['problem_description']
            priority = request.form['priority']

            attachment_file = request.files.get('attachment')
            attachment_path = None
            if attachment_file and attachment_file.filename != "":
                filename = secure_filename(attachment_file.filename)
                os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                attachment_path = os.path.join(UPLOAD_FOLDER, filename)
                attachment_file.save(attachment_path)

            # ✅ Pass created_by to support_ticket model function
            create_support_ticket(
                dept_id,
                comments,
                problem_description,
                priority,
                attachment_path,
                user["id"]  # ✅ created_by
            )

            flash("✅ Support ticket created successfully!", "success")
            return redirect(url_for('test_routes.test_tasks'))

        departments = get_all_departments()
        return render_template('employee/create_support_ticket.html', departments=departments, user=user)
        return render_template('employee/create_support_ticket.html', departments=departments,user=user)