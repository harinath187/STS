import os
from flask import render_template, request, current_app, url_for, redirect, flash, send_from_directory
from app.models.task_comments import insert_task_comment

def register_task_comments_routes(app):
    # Configure upload folder
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'chumma')
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    @app.route('/create_task_comment', methods=['GET', 'POST'])
    def create_task_comment():
        if request.method == 'POST':
            task_id = request.form['task_id']
            message = request.form['message']
            file = request.files.get('attachment')

            # insert into DB and save file
            filename = insert_task_comment(task_id, message, file, app.config['UPLOAD_FOLDER'])

            flash("Task comment created successfully!", "success")
            return redirect(url_for('test_routes.test_tasks')) 

        # Correct template path
        return render_template('employee/create_task_comment.html')

    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
