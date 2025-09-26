from app import app


# Import other route files
from app.routes import due_today
from flask import Flask,render_template, request
from app.models.due_today import get_today_task,get_all_task,get_pending_task,get_completed_task,get_task_by_date, over_due_task

app = Flask(__name__,template_folder='../templates')

@app.route("/")
def html_file():
    
    # print("task must show here.............",today_task)
    return render_template("due_today.html")


@app.route("/task")
def get_today_task_route():
    today_task = get_today_task()
    # print("task must show here.............",today_task)
    return render_template("due_today.html",today_task = today_task)

@app.route("/all_task")
def get_all_task_route():
    all_task = get_all_task()
    return render_template("due_today.html",today_task = all_task)

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
    print(a)
    get_date = get_task_by_date(a)
    print("geting_data",get_date)
    return render_template("due_today.html",today_task = get_date)

@app.route("/overdue_task")
def overdue():
    get_overdue = over_due_task()
    return render_template("due_today.html",today_task = get_overdue)



