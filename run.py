from app import create_app
from flask import session
app = create_app()


@app.context_processor
def inject_user():
    return dict(user=session.get("user"))

if __name__ == "__main__":
    print("Template folder is:", app.template_folder)
    print("Static folder is:", app.static_folder)
    app.run(debug=True)
