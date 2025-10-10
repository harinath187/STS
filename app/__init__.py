import os
from flask import Flask
from app.routes.openticket_routes import register_open_ticket_routes

# Existing route imports
from app.routes.login_routes import register_routes
from app.routes.emp_dashboard_routes import register_employee_routes
from app.routes.test import test_routes  # Blueprint
from app.routes.support_ticket_routes import register_support_ticket_routes
from app.routes.task_comment_routes import register_task_comments_routes
from app.routes.support_comment_routes import register_support_comment_routes
from app.routes.it_manager_routes import register_support_routes
from app.routes.register_it_employee_routes import register_it_employee_routes
from app.routes.project_routes import project_bp
from app.routes.task_update_routes import register_task_update_routes
from app.routes.Project_routes import register_project_routes
from app.routes.hrroute import (
    employeeslist,
    updateemplist,
    addemployee,
    add_employeelist,
    add_client_list,
    add_client,
    list_client,delete_client
,update_get_client,update_post_client)  # sai added
from app.routes.supporthistoryroute import (
    supporthistory,
    suppassignlist,
    notsuppassignlist,
    ticket_detail_route,
    ticket_delete_route,
    employee_routes  
)
from app.routes.manager_routes import register_manager_routes

# New import for Project Task blueprint
from app.routes.project_task_routes import task_bp


def create_app():
    app = Flask(__name__)
    app.secret_key = "sts"

    # Register all major routes
    register_routes(app)
    register_employee_routes(app)
    register_support_ticket_routes(app)
    register_task_comments_routes(app)
    register_support_comment_routes(app)
    # Register open ticket routes separately
    register_open_ticket_routes(app)
    app.register_blueprint(test_routes)
    register_project_routes(app)
    register_support_routes(app)
    register_manager_routes(app)
    register_it_employee_routes(app)

    # Blueprints

    app.register_blueprint(project_bp)
    app.register_blueprint(task_bp)   # added for project task module

    # Support history & HR routes
    supporthistory(app)
    suppassignlist(app)
    notsuppassignlist(app)
    employeeslist(app)
    updateemplist(app)
    addemployee(app)
    add_employeelist(app)
    add_client_list(app)
    list_client(app)
    add_client(app)
    delete_client(app)
    update_get_client(app)
    update_post_client(app)

    # Ticket detail/edit/delete routes
    ticket_detail_route(app)
    register_task_update_routes(app)
    ticket_delete_route(app)

    # Employee dropdown routes
    employee_routes(app)

    return app
