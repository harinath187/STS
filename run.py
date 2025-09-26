

# from app import create_app

# app = create_app()

# if __name__ == "__main__":
#     app.run(debug=True)

# run.py
from flask import Flask, render_template
from STS.app.models.mytickets import get_tasks_by_employee
from app.routes.employee.mytickets_routes import show_my_tasks

app = Flask(__name__)

# Registering the route directly in run.py
@app.route('/my-tasks/<int:emp_id>')
def show_my_tasks_route(emp_id):
    return show_my_tasks(emp_id)

if __name__ == '__main__':
    app.run(debug=True)
