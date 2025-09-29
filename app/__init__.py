

from flask import Flask
from app.routes.login_routes import register_routes
from app.routes import project_task_routes
def create_app():
    app = Flask(__name__)
    app.secret_key = "sts"  


    
    from app.routes.project_task_routes import task_bp
    print("ssssssss")
    app.register_blueprint(task_bp)

    register_routes(app)

    return app
