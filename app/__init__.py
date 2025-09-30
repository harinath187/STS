from flask import Flask
from app.routes.login_routes import register_routes
from app.routes.emp_dashboard_routes import register_employee_routes
from app.routes.test import test_routes  # Blueprint
from app.routes.support_ticket_routes import register_support_ticket_routes
from app.routes.task_comment_routes import register_task_comments_routes
from app.routes.support_comment_routes import register_support_comment_routes  # <-- new
from app.routes.it_manager_routes import register_support_routes
from app.routes.test import test_routes  # ✅ Add this
from app.routes.emp_dashboard_routes import register_employee_routes
from app.routes.supporthistoryroute import supporthistory,suppassignlist,notsuppassignlist
def create_app():
    app = Flask(__name__)
    app.secret_key = "sts"

    # Register all routes
    register_routes(app)
    register_employee_routes(app)
    register_support_ticket_routes(app)
    register_task_comments_routes(app)
    register_support_comment_routes(app) 
    app.register_blueprint(test_routes)

    register_support_routes(app)


    supporthistory(app)
    suppassignlist(app)
    notsuppassignlist(app)

    return app

