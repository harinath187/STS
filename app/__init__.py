
import os
from flask import Flask
from app.routes.project_routes import project_bp
from app.routes.login_routes import register_routes

def create_app():
    app = Flask(__name__)
    app.secret_key = "sts"
    upload_folder = 'static/uploads'
    app.config['UPLOAD_FOLDER'] = upload_folder
    os.makedirs(upload_folder, exist_ok=True)   
    app.register_blueprint(project_bp)
    register_routes(app)

    return app
