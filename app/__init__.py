import os
from flask import Flask
from app.routes.login_routes import register_routes
from app.routes.emp_dashboard_routes import register_employee_routes
from app.routes.test import test_routes
from app.routes.support_ticket_routes import register_support_ticket_routes
from app.routes.task_comment_routes import register_task_comments_routes
from app.routes.support_comment_routes import register_support_comment_routes
from app.routes.it_manager_routes import register_support_routes
from app.routes.register_it_employee_routes import register_it_employee_routes
<<<<<<< HEAD
from app.routes.test import test_routes
from app.routes.emp_dashboard_routes import register_employee_routes
from app.routes.hrroute import employeeslist,updateemplist,addemployee,add_employeelist #sai added
=======
>>>>>>> d462707 (all crud to project dash)
from app.routes.supporthistoryroute import (
    supporthistory,
    suppassignlist,
    notsuppassignlist,
    ticket_detail_route,
    ticket_delete_route,
    employee_routes
)
from app.routes.manager_routes import register_manager_routes

# NEW PROJECT TASK ROUTES
from app.routes.project_task_routes import task_bp
from app.routes.project_dashboard_routes import project_dashboard_bp

def create_app():
    app = Flask(__name__)
    app.secret_key = "sts"
    
    # Register all existing routes
    register_routes(app)
    register_employee_routes(app)
    register_support_ticket_routes(app)
    register_task_comments_routes(app)
    register_support_comment_routes(app)
    app.register_blueprint(test_routes)
    register_support_routes(app)
    
    # Support history routes
    supporthistory(app)
    suppassignlist(app)
    notsuppassignlist(app)
<<<<<<< HEAD
    employeeslist(app)
    updateemplist(app)
    addemployee(app)
    add_employeelist(app)

    # Ticket detail/edit/delete routes
=======
>>>>>>> d462707 (all crud to project dash)
    ticket_detail_route(app)
    ticket_delete_route(app)
    employee_routes(app)
    
    # Manager dashboard routes
    register_manager_routes(app)
    register_it_employee_routes(app)
    
    # NEW: Project Task Management Routes
    app.register_blueprint(task_bp)
    app.register_blueprint(project_dashboard_bp)
    
    return app