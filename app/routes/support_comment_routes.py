import os
from flask import render_template, request, redirect, flash, url_for, send_from_directory, session
from app.models.support_comments import insert_support_comment

def register_support_comment_routes(app):
    # Upload folder config
    upload_folder = os.path.join(app.root_path, 'support_uploads')
    os.makedirs(upload_folder, exist_ok=True)

    @app.route('/create_support_comment', methods=['GET', 'POST'])
    def create_support_comment():
        user = session.get("user")
        if not user:
            return redirect("/login")
        if request.method == 'POST':
            supt_id = request.form['supt_id']
            message = request.form['message']
            file = request.files.get('attachment')

            filename = insert_support_comment(supt_id, message, file, upload_folder)

            flash("✅ Support ticket comment created successfully!","success")
            return redirect(url_for('create_support_comment'))  # redirect to the same page or a list page

        return render_template('employee/create_support_comment.html',user=user)

    @app.route('/support_uploads/<filename>')
    def uploaded_support_file(filename):
        return send_from_directory(upload_folder, filename)
