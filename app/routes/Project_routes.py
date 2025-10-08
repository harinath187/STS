# Import other route files
#from app.routes import due_today

import os
from flask import Blueprint, render_template, request, redirect, flash, current_app,session,Blueprint,jsonify,url_for,session
from werkzeug.utils import secure_filename
from app.models.project_models import fetch_all_projects, insert_project,update_project_model,delete_project_by_id
from app.models.db import get_db_connection

from app.models.project_db import get_today_task,get_all_task,get_pending_task,get_completed_task,get_task_by_date, over_due_task
from app.models.client import get_client_name


# app = Blueprint('app', __name__)
def register_project_routes(app):
    @app.route("/get_client_data")
    
    def get_dropdown_data():
        # print("here data come..........")
        client_name = get_client_name()
        # a = user["id"]
        # print(a)
        # print(f'{user["firstname"]} {user["lastname"]}')
        # print("client_name...........",client_name)
        return client_name 



    
    @app.route("/task")
    def html_file():
        
        return render_template("project_management/due_today.html")


    @app.route("/today_task")
    def get_today_task_route():
        today_task = get_today_task()
        
        return render_template("project_management/due_today.html",today_task = today_task)

    @app.route("/all_task")
    def get_all_task_route():
        print("all Task ..............")
        all_task = get_all_task()
        return render_template("project_management/due_today.html",today_task = all_task)

    @app.route("/pending_task")
    def get_pending_task_route():
        all_task = get_pending_task()
        return render_template("due_today.html",today_task = all_task)


    @app.route("/completed_task")
    def get_completed_task_route():
        all_task = get_completed_task()
        return render_template("due_today.html",today_task = all_task)

    @app.route("/get_task_date", methods=['POST'])
    def get_by_task_date_route():
        a = request.form.get("selectedDate")
        get_date = get_task_by_date(a)
        # print("geting_data",get_date)
        return render_template("due_today.html",today_task = get_date)

    @app.route("/overdue_task")
    def overdue():
        get_overdue = over_due_task()
        return render_template("due_today.html",today_task = get_overdue)

    @app.route('/save_project', methods=['GET', 'POST'])
    def add_project():
        user = session.get("user")
        clients = get_dropdown_data()
       
        # print("project_added getting data............")
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
            print("Project_details...............", form_data)
            success = insert_project(form_data)
            if success:
                flash("Project added successfully!", "success")
                return redirect('/projects')
            else:
                flash("Failed to add project.", "error")

        return render_template('mypro/add_project.html', client_name=clients, user=user)




    @app.route('/projects')
    def show_projects():
        pm = session.get("user")
        print("dtrfdsfgdsfdgdgdgf",pm)
        projects = fetch_all_projects()
        return render_template('mypro/project_list.html', projects=projects, user=pm)

    UPLOAD_FOLDER = 'static/uploads'

   
    




    @app.route('/update_project/<int:project_id>', methods=['GET'])
    def edit_project(project_id):
        user=session.get("user")
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        # print("project iddddd.......",project_id)


        cursor.execute("SELECT * FROM project WHERE id=%s", (project_id,))
        project = cursor.fetchone()

       
        cursor.execute("SELECT client_id, Company_Name FROM Client_Details")
        clients = cursor.fetchall()

        cursor.close()
        conn.close()


        return render_template('mypro/update_project.html', project=project, client_name=clients,user=user)


    
    @app.route('/update_project/<int:project_id>', methods=['POST'])
    def update_project(project_id):
        # print("project idiiii.......",project_id)
        conn = get_db_connection()
        try:    
            cursor = conn.cursor()

            print("Form data:", request.form)
            print("Files:", request.files)

            project_name = request.form.get('project_name', '').strip()
            client_name = request.form.get('client_name', '')
            estimated_duration = request.form.get('estimated_duration', 0)
            tech_stack = request.form.get('tech_stack', '')
            time_taken = request.form.get('time_taken', 0)
            cost_hours = request.form.get('cost_hours', 0)
            status_percentage = request.form.get('status_percentage', 0)
            # print(".....................",estimated_duration)
            attachments = request.files.getlist('attachments')
            attachment_names = ','.join([f.filename for f in attachments]) if attachments else ''

            cursor.execute("""
                UPDATE project
                SET project_name=%s, client_id=%s, estimated_duration_months=%s, tech_stack=%s,
                    actual_time_taken=%s, cost_hours=%s, status_percentage=%s,
                    Attachment=%s
                WHERE id=%s
            """, (project_name, client_name, estimated_duration, tech_stack,
                time_taken, cost_hours, status_percentage, attachment_names, project_id))

            conn.commit()
            cursor.execute("""
                SELECT p.id, p.project_name, c.Company_Name AS client_name, 
                    p.estimated_duration_months, p.tech_stack, p.actual_time_taken, 
                    p.cost_hours, p.status_percentage
                FROM project p
                LEFT JOIN Client_Details c ON p.client_id = c.client_id
            """)
            projects = cursor.fetchall()
        except Exception as e:
            print(" Error fetching projects:", e)
            return []
        finally:
        
            cursor.close()
            conn.close()

        return redirect(url_for('show_projects'))

    
    @app.route("/project/delete/<int:project_id>")
    def delete_project(project_id):
        delete_project_by_id(project_id)
        # flash("project deleted successfully!", "success")
        return redirect(url_for("show_projects"))
