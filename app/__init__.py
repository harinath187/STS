<<<<<<< HEAD


from flask import Flask

<<<<<<< HEAD
from app.routes.project_routes import project_bp

from app.routes.login_routes import register_routes
<<<<<<< HEAD

=======
=======
=======
<<<<<<< HEAD
from flask import Flask

=======

import os
from flask import Flask
from app.routes.project_routes import project_bp
>>>>>>> b18dc26 (some changes)
>>>>>>> 869aa60 (some changes)
from app.routes.login_routes import register_routes

from app.routes.it_manager_routes import register_support_routes
>>>>>>> 10c6969 (solamaten)
from app.routes.test import test_routes  # ✅ Add this
from app.routes.emp_dashboard_routes import register_employee_routes
from app.routes.supporthistoryroute import supporthistory,suppassignlist,notsuppassignlist
>>>>>>> 8783371 (updated code of support history)
def create_app():
    app = Flask(__name__)
<<<<<<< HEAD
    app.secret_key = "sts"
    upload_folder = 'static/uploads'
    app.config['UPLOAD_FOLDER'] = upload_folder
    os.makedirs(upload_folder, exist_ok=True)   
    app.register_blueprint(project_bpp)
=======
<<<<<<< HEAD
    app.secret_key = "sts"  
>>>>>>> 869aa60 (some changes)

<<<<<<< HEAD
    register_routes(app)

=======
    # Register all routes
    register_routes(app)  # login, admin, etc.
    register_employee_routes(app)  # employee dashboard routes
    test_routes(app)
    supporthistory(app)
    suppassignlist(app)
    notsuppassignlist(app)
<<<<<<< HEAD
>>>>>>> 8783371 (updated code of support history)
=======
=======
    app.secret_key = "sts"
    upload_folder = 'static/uploads'
    app.config['UPLOAD_FOLDER'] = upload_folder
    os.makedirs(upload_folder, exist_ok=True)   
    app.register_blueprint(project_bp)
    register_routes(app)
>>>>>>> b18dc26 (some changes)

>>>>>>> 869aa60 (some changes)
    return app


from app.routes import Project_routes

def create_app():
    app = Flask(__name__)
    app.secret_key = "sts"  
    register_routes(app)

