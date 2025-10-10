
import os
from flask import Blueprint, render_template, request, redirect, flash, current_app,session,url_for
from werkzeug.utils import secure_filename
from app.models.project_models import fetch_all_projects, insert_project,get_employees_assigned_by
from app.models.db import get_db_connection

project_bp = Blueprint('project_bp', __name__)

@project_bp.route('/projects')
def show_projects():
    projects = fetch_all_projects()
    return render_template('mypro/project_list.html', projects=projects)

UPLOAD_FOLDER = 'static/uploads'

# @project_bp.route('/save_project', methods=['GET', 'POST'])
# def add_project():
#     if request.method == 'POST':
#         form_data = request.form.to_dict()
#         file = request.files.get('attachment')

#         upload_folder = current_app.config['UPLOAD_FOLDER']
#         os.makedirs(upload_folder, exist_ok=True)

#         if file and file.filename:
#             filename = secure_filename(file.filename)
#             filepath = os.path.join(upload_folder, filename)
#             file.save(filepath)
#             form_data['Attachment'] = filepath
#         else:
#             form_data['Attachment'] = None

#         success = insert_project(form_data)
#         if success:
#             flash("Project added successfully!", "success")
#             return redirect('/projects')
#         else:
#             flash("Failed to add project.", "error")

#     return render_template('mypro/add_project.html')



@project_bp.route("/project_manager/team")
def project_manager_team():
    user = session.get("user")
    if not user or user.get("dept_id") != 3:
        return redirect(url_for("login"))
 
    manager_id = user.get("id")
    team_members = get_employees_assigned_by(manager_id)
 
    return render_template(
        "mypro/project_team.html",
        user=user,
        team_members=team_members
    )