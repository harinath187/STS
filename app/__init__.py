

from flask import Flask

from app.routes.login_routes import register_routes
from app.routes import Project_routes

def create_app():
    app = Flask(__name__)
    app.secret_key = "sts"  
    register_routes(app)
    
