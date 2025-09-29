import os
from flask import Flask
from app.routes.login_routes import register_routes
from app.routes.manager_routes import manager_bp


base_dir = os.path.dirname(__file__)
template_dir = os.path.join(base_dir, "app", "templates")
static_dir = os.path.join(base_dir, "app", "static")

app = Flask(
    __name__, 
    template_folder=template_dir, 
    static_folder=static_dir
)

#application secret key
app.secret_key = "your-secret-key"

# Register routes
register_routes(app)
app.register_blueprint(manager_bp)

if __name__ == "__main__":
    print("Template folder is:", app.template_folder)
    print("Static folder is:", app.static_folder)
    app.run(debug=True) 
    