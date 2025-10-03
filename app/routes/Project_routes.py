


# Import other route files
#from app.routes import due_today
import os
from flask import Blueprint, render_template, request, redirect, flash, current_app
from flask import Flask,render_template, request, Blueprint
from werkzeug.utils import secure_filename
from app.models.project_models import fetch_all_projects, insert_project

from app.models.project_db import get_today_task,get_all_task,get_pending_task,get_completed_task,get_task_by_date, over_due_task
from app.models.client import get_client_name


project_bpp = Blueprint('project_bpp', __name__)


def get_dropdown_data():
    client_name = get_client_name()
    print("client_name...........",client_name)
    return render_template("mypro/add_project.html",client_name = client_name)



@project_bpp.route("/task")
def html_file():
    # print("task must show here.............",today_task)
    return render_template("project_management/due_today.html")


@project_bpp.route("/today_task")
def get_today_task_route():
    today_task = get_today_task()
    # print("task must show here.............",today_task)
    return render_template("project_management/due_today.html",today_task = today_task)

@project_bpp.route("/all_task")
def get_all_task_route():
    all_task = get_all_task()
    return render_template("project_management/due_today.html",today_task = all_task)

@project_bpp.route("/pending_task")
def get_pending_task_route():
    all_task = get_pending_task()
    return render_template("due_today.html",today_task = all_task)


@project_bpp.route("/completed_task")
def get_completed_task_route():
    all_task = get_completed_task()
    return render_template("due_today.html",today_task = all_task)

@project_bpp.route("/get_task_date", methods=['POST'])
def get_by_task_date_route():
    a = request.form.get("selectedDate")
    get_date = get_task_by_date(a)
    # print("geting_data",get_date)
    return render_template("due_today.html",today_task = get_date)

@project_bpp.route("/overdue_task")
def overdue():
    get_overdue = over_due_task()
    return render_template("due_today.html",today_task = get_overdue)

@project_bpp.route('/save_project', methods=['GET', 'POST'])
def add_project():
    if request.method == 'POST':
        form_data = request.form.to_dict()
        file = request.files.get('attachment')

        upload_folder = current_app.config['UPLOAD_FOLDER']
        os.makedirs(upload_folder, exist_ok=True)
        print("Project_details...............", form_data)
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



