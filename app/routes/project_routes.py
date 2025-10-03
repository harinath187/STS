import os
from flask import Blueprint, render_template, request, redirect, flash, current_app, session ,url_for
from werkzeug.utils import secure_filename
from app.models.project_models import insert_project, fetch_projects_by_pm, fetch_team_tasks_under_pm
from flask import send_from_directory
from app.models.project_models import count_projects_by_pm



project_bp = Blueprint('project_bp', __name__)

@project_bp.route('/projects')
def show_projects():
    user = session.get("user")
    if not user:
        return redirect(url_for("auth_bp.login")) 

    user_id = user.get("id") 
    projects = fetch_projects_by_pm(user_id)
    return render_template('mypro/project_list.html', projects=projects, user=user)

@project_bp.route('/projects/add', methods=['GET', 'POST'])
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
    user = session.get("user")
    print(user)
    if not user:
        flash("You must be logged in to view your project count.", "error")
        return redirect('/login')

    project_count = count_projects_by_pm(user["username"])
    print(project_count)
    return render_template('mypro/project_count.html', user=user, count=project_count)



@project_bp.route('/team-tasks')
def show_team_tasks():
    user = session.get("user")
    if not user:
        return redirect(url_for("auth_bp.login"))

    pm_id = user.get("id")
    team_tasks = fetch_team_tasks_under_pm(pm_id)
    print(team_tasks)
    return render_template("mypro/project_count.html", team_tasks=team_tasks, user=user)