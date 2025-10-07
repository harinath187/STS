from flask import render_template
from app.utils.auth import login_required 

def test_routes(app):
    @app.route("/tickets")
    @login_required  
    def test():
        return render_template("employee/test.html")
