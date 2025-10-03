
import os
from flask import Flask
import os
from app.routes.Project_routes import project_bpp
from app.routes.emp_dashboard_routes import register_employee_routes

from app.routes.project_routes import project_bp

from app.routes.login_routes import register_routes

from app.routes.it_manager_routes import register_support_routes
from app.routes.test import test_routes  # ✅ Add this
from app.routes.emp_dashboard_routes import register_employee_routes
from app.routes.supporthistoryroute import supporthistory,suppassignlist,notsuppassignlist
def create_app():
    app = Flask(__name__)

    app.secret_key = "sts"
    upload_folder = 'static/uploads'
    app.config['UPLOAD_FOLDER'] = upload_folder
    os.makedirs(upload_folder, exist_ok=True)   

    app.register_blueprint(project_bpp)
    register_employee_routes(app)
    register_routes(app)


    app.register_blueprint(project_bp) # login, admin, etc.
    register_employee_routes(app)  # employee dashboard routes
    test_routes(app)
    supporthistory(app)
    suppassignlist(app)
    notsuppassignlist(app)

    return app

