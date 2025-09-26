
import os
from flask import Blueprint, render_template, request, redirect, flash, current_app
from werkzeug.utils import secure_filename
from app.models.project_models import fetch_all_projects, insert_project


project_bp = Blueprint('project_bp', __name__)

@project_bp.route('/projects')
def show_projects():
    projects = fetch_all_projects()
    return render_template('mypro/project_list.html', projects=projects)

UPLOAD_FOLDER = 'static/uploads'

@project_bp.route('/projects/add', methods=['GET', 'POST'])
def add_project():
    if request.method == 'POST':
        form_data = request.form.to_dict()
        file = request.files.get('attachment')

        upload_folder = current_app.config['UPLOAD_FOLDER']
        os.makedirs(upload_folder, exist_ok=True)

        if file and file.filename:
            filename = secure_filename(file.filename)
            filepath = os.path.join(upload_folder, filename)
            file.save(filepath)
            form_data['Attachment'] = filepath
        else:
            form_data['Attachment'] = None

        success = insert_project(form_data)
        if success:
            flash("Project added successfully!", "success")
            return redirect('/projects')
        else:
            flash("Failed to add project.", "error")

    return render_template('mypro/add_project.html')
