import os
from flask import Blueprint, render_template, request, redirect, flash, current_app, session, url_for, send_from_directory
from werkzeug.utils import secure_filename
from app.models.project_models import insert_project, count_projects_by_pm ,fetch_projects_by_pm

project_bp = Blueprint('project_bp', __name__)


@project_bp.route('/projects')
def show_projects():
    pm = session.get("user") 
    print(pm)
    projects = fetch_projects_by_pm(pm["id"])
    full_name = pm["firstname"]+pm["lastname"] 

    return render_template('mypro/project_list.html', projects=projects, user=pm)


@project_bp.route('/projects/add', methods=[ 'POST'])
def add_project():
    if request.method == 'POST':
        form_data = request.form.to_dict()
        file = request.files.get('attachment')

        upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)

        if file and file.filename:
            filename = secure_filename(file.filename)
            filepath = os.path.join(upload_folder, filename)
            file.save(filepath)

            form_data['Attachment'] = f"uploads/{filename}"

            print(f"[UPLOAD] Saved to: {filepath}")
            print(f"[UPLOAD] Stored path: {form_data['Attachment']}")
        else:
            form_data['Attachment'] = None

        success = insert_project(form_data)
        flash("Project added successfully!" if success else "Failed to add project.", "success" if success else "error")
        return redirect('/projects')

    return render_template('mypro/add_project.html')


@project_bp.route('/upload/<filename>')
def serve_uploaded_file(filename):
    upload_folder = current_app.config.get('UPLOAD_FOLDER', os.path.join('static', 'uploads'))
    return send_from_directory(upload_folder, filename)

@project_bp.route('/projects/count')
def count_pm_projects():
    raw_user = session.get("user")
    if not raw_user or not isinstance(raw_user, dict) or "username" not in raw_user:
        flash("You must be logged in to view your project count.", "error")
        return redirect('/login')

    pm_name = raw_user["username"].strip()
    project_count = count_projects_by_pm(pm_name)

    return render_template('mypro/project_count.html', user=raw_user, count=project_count)