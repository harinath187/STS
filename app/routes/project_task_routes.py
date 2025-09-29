from flask import Blueprint, render_template, request, redirect, url_for
from app.models.project_task import ProjectTask
print("sssssssss")
task_bp = Blueprint('task_bp', __name__)


@task_bp.route('/task', methods=['GET'])
def list_tasks():
    print("ssssssssssss1")
    projects = ProjectTask.fetch_all_projects()
    selected_project_id = request.args.get('project_id')
    search_name = request.args.get('task_name')

    if search_name:  
        tasks = ProjectTask.fetch_tasks_by_name(search_name)
    elif selected_project_id: 
        tasks = ProjectTask.fetch_tasks_by_project(selected_project_id)
    else:
        tasks = []

    return render_template(
        'list_task.html',
        tasks=tasks,
        projects=projects,
        selected_project_id=selected_project_id,
        search_name=search_name
    )


@task_bp.route('/tasks/add', methods=['GET', 'POST'])
def add_task():
    projects = ProjectTask.fetch_all_projects()
    if request.method == 'POST':
        project_id = request.form.get('project_id')
        task_name = request.form.get('task_name')
        task_description = request.form.get('task_description')
        task_duration = request.form.get('task_duration') 
        status = request.form.get('status', 'PENDING')
        ProjectTask.add_task(project_id, task_name, task_description, task_duration, status)
        return redirect(url_for('task_bp.list_tasks', project_id=project_id))
    
    return render_template('add_task.html', projects=projects)
 
