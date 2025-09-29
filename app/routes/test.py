from flask import render_template
from app.utils.auth import login_required  # <- import once

def test_routes(app):
    @app.route("/tickets")
    @login_required  # ✅ This replaces the if-check!
    def test():
        return render_template("employee/test.html")
