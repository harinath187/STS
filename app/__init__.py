

from flask import Flask
import os
from app.routes.Project_routes import project_bpp
from app.routes.emp_dashboard_routes import register_employee_routes
from app.routes.login_routes import register_routes

def create_app():
    app = Flask(__name__)
    app.secret_key = "sts"
    upload_folder = 'static/uploads'
    app.config['UPLOAD_FOLDER'] = upload_folder
    os.makedirs(upload_folder, exist_ok=True)   
    app.register_blueprint(project_bpp)
    register_employee_routes(app)
    register_routes(app)

    return app

