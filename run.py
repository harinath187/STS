from app import create_app
app = create_app()

if __name__ == "__main__":
    print("Template folder is:", app.template_folder)
    print("Static folder is:", app.static_folder)
    app.run(debug=True) 
    