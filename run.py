from app import create_app
app = create_app()

# if __name__ == "__main__":
#     app.run(debug=True)
if __name__ == '__main__':

    app.run(debug=True, port=8089)

if __name__ == "__main__":
    print("Template folder is:", app.template_folder)
    print("Static folder is:", app.static_folder)
    app.run(debug=True) 
@app.context_processor
def inject_user():
    from flask import session
    return dict(user=session.get("user"))