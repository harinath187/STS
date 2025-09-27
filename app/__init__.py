from flask import Flask
from app.routes.login_routes import register_routes
from app.routes.test import test_routes  # ✅ Add this
from app.routes.emp_dashboard_routes import register_employee_routes

def create_app():
    app = Flask(__name__)
    app.secret_key = "sts"  

    # Register all routes
    register_routes(app)  # login, admin, etc.
    register_employee_routes(app)  # employee dashboard routes
    test_routes(app)

    return app
