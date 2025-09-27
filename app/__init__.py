from flask import Flask
from app.routes.login_routes import register_routes
from app.routes.emp_dashboard_routes import register_employee_routes
from app.routes.test import test_routes  # Blueprint

def create_app():
    app = Flask(__name__)
    app.secret_key = "sts"

    # Register all routes
    register_routes(app)
    register_employee_routes(app)
    app.register_blueprint(test_routes)  # ✅ register blueprint

    return app
