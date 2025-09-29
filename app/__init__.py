from flask import Flask
from app.routes.login_routes import register_routes
<<<<<<< HEAD
from app.routes import project_task_routes
=======
from app.routes.it_manager_routes import register_support_routes
from app.routes.test import test_routes  # ✅ Add this
from app.routes.emp_dashboard_routes import register_employee_routes

>>>>>>> 05cf511a98673a18b22da3fa199e7026b22a4ec6
def create_app():
    app = Flask(__name__)
    app.secret_key = "sts"  

<<<<<<< HEAD

    
    from app.routes.project_task_routes import task_bp
    print("ssssssss")
    app.register_blueprint(task_bp)

    register_routes(app)
=======
    # Register all routes
    register_routes(app)  # login, admin, etc.
    register_employee_routes(app)  # employee dashboard routes
    test_routes(app)
    register_support_routes(app)
>>>>>>> 05cf511a98673a18b22da3fa199e7026b22a4ec6

    return app

