

from flask import Flask
from app.routes.project_routes import project_bp
from app.routes.login_routes import register_routes
from app.routes.it_manager_routes import register_support_routes
from app.routes.test import test_routes  # ✅ Add this
from app.routes.emp_dashboard_routes import register_employee_routes

def create_app():
    app = Flask(__name__)
    app.secret_key = "sts"  

    register_routes(app)

    return app

