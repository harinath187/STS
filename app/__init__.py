from flask import Flask
from app.routes.login_routes import register_routes
from app.routes.it_manager_routes import register_support_routes
from app.routes.test import test_routes
from app.routes.emp_dashboard_routes import register_employee_routes

def create_app():
    app = Flask(__name__)
    app.secret_key = "sts"
    
    # Project Task CRUD Blueprint
    from app.routes.project_task_routes import task_bp
    app.register_blueprint(task_bp)
    
    # Project Dashboard Blueprint
    from app.routes.project_dashboard_routes import project_dashboard_bp
    app.register_blueprint(project_dashboard_bp)
    
    # Register other routes
    register_routes(app)
    register_employee_routes(app)
    test_routes(app)
    register_support_routes(app)
    
    return app