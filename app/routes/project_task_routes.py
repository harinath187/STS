from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.project_task import ProjectTask
import os
from werkzeug.utils import secure_filename
from app.utils.auth import login_required

task_bp = Blueprint('task_bp', __name__)

UPLOAD_FOLDER = 'app/static/uploads/task_attachments'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# -------------------- List Tasks --------------------
@task_bp.route('/task', methods=['GET'])
@login_required
def list_tasks():
    projects = ProjectTask.fetch_all_projects()
    selected_project_id = request.args.get('project_id')
    search_name = request.args.get('task_name')

    if search_name:  
        tasks = ProjectTask.fetch_tasks_by_name(search_name)
    elif selected_project_id: 
        tasks = ProjectTask.fetch_tasks_by_project(selected_project_id)
    else:
        tasks = []

    # Fix attachments path
    for task in tasks:
        if task.get("attachments"):
            attachment_path = task["attachments"]
            if "app/static/" in attachment_path:
                task["attachments"] = attachment_path.split("app/static/")[1]
            elif "static/" in attachment_path:
                task["attachments"] = attachment_path.split("static/")[1]

    # Pass user from session to template
    user = session.get('user')

    return render_template(
        'project_task/list_task.html',
        tasks=tasks,
        projects=projects,
        selected_project_id=selected_project_id,
        search_name=search_name,
        user=user
    )


# -------------------- Add Task --------------------
@task_bp.route('/tasks/add', methods=['GET', 'POST'])
@login_required
def add_task():
    projects = ProjectTask.fetch_all_projects()
    employees = ProjectTask.fetch_all_employees()
    user = session.get('user')

    if request.method == 'POST':
        project_id = request.form.get('project_id')
        task_name = request.form.get('task_name')
        task_description = request.form.get('task_description')
        task_duration = request.form.get('task_duration')
        assigned_to = request.form.get('assigned_to')
        assigned_by = request.form.get('assigned_by')
        estimated_hrs = request.form.get('estimated_hrs')
        worked_hrs = request.form.get('worked_hrs', 0)
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        comments = request.form.get('comments')
        status = request.form.get('status', 'PENDING')
        
        attachment_path = None
        if 'attachment' in request.files:
            file = request.files['attachment']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                file.save(file_path)
                attachment_path = file_path
        
        ProjectTask.add_task(
            project_id, task_name, task_description, task_duration,
            assigned_to, assigned_by, estimated_hrs, worked_hrs,
            start_date, end_date, comments, status, attachment_path
        )
        flash('Task created successfully!', 'success')
        return redirect(url_for('task_bp.list_tasks', project_id=project_id))
    
    return render_template('project_task/add_task.html', projects=projects, employees=employees, user=user)


# -------------------- Edit Task --------------------
@task_bp.route('/tasks/edit/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    task = ProjectTask.get_task_by_id(task_id)
    if not task:
        flash('Task not found!', 'danger')
        return redirect(url_for('task_bp.list_tasks'))
    
    projects = ProjectTask.fetch_all_projects()
    employees = ProjectTask.fetch_all_employees()
    user = session.get('user')
    
    if request.method == 'POST':
        project_id = request.form.get('project_id')
        task_name = request.form.get('task_name')
        task_description = request.form.get('task_description')
        task_duration = request.form.get('task_duration')
        assigned_to = request.form.get('assigned_to')
        assigned_by = request.form.get('assigned_by')
        estimated_hrs = request.form.get('estimated_hrs')
        worked_hrs = request.form.get('worked_hrs')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        comments = request.form.get('comments')
        status = request.form.get('status')
        
        attachment_path = task.get('attachments')
        if 'attachment' in request.files:
            file = request.files['attachment']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                file.save(file_path)
                attachment_path = file_path
        
        ProjectTask.update_task(
            task_id, project_id, task_name, task_description, task_duration,
            assigned_to, assigned_by, estimated_hrs, worked_hrs,
            start_date, end_date, comments, status, attachment_path
        )
        flash('Task updated successfully!', 'success')
        return redirect(url_for('task_bp.list_tasks', project_id=project_id))
    
    return render_template('project_task/edit_task.html', task=task, projects=projects, employees=employees, user=user)


# -------------------- Delete Task --------------------
@task_bp.route('/tasks/delete/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    task = ProjectTask.get_task_by_id(task_id)
    if task:
        project_id = task['project_id']
        ProjectTask.delete_task(task_id)
        flash('Task deleted successfully!', 'success')
        return redirect(url_for('task_bp.list_tasks', project_id=project_id))
    else:
        flash('Task not found!', 'danger')
        return redirect(url_for('task_bp.list_tasks'))


# -------------------- Back to Dashboard --------------------
@task_bp.route('/back-to-dashboard')
@login_required
def back_to_dashboard():
    # Make sure this matches your actual endpoint name in manager_bp
    return redirect(url_for('manager_bp.it_manager_dashboard'))