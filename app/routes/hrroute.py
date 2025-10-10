from flask import render_template, request, redirect, url_for, flash,session
from app.utils.auth import login_required
from app.models.hr import employeelist,departmentlist,roleslist
from app.models.db import get_db_connection 

def employeeslist(app):
    @app.route("/employeeslist")
    @login_required
    def emplist():
        listitem = employeelist()
        department=departmentlist()
        roles=roleslist()
        print(department)
        print(roles)
        user = session.get("user")
        return render_template("hr/list_of_employees.html", employeelist=listitem,dept_list=department,role=roles, user=user)

def addemployee(app):
    @app.route("/addemployee") 
    @login_required 
    def add_emplist():
        department=departmentlist()
        roles=roleslist()
        user = session.get("user")
        return render_template("hr/Addemployee.html",dept_list=department,role=roles,user=user)

def updateemplist(app):
    @app.route('/update_employee', methods=['POST'])
    @login_required
    def uplist():
        emp_id = request.form['id']

        email = request.form['email']
        dept_id = request.form['dept_id']       
        role_id = request.form['role_id']      
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            UPDATE employee
            SET 
                email=%s,
                dept_id=%s,
                role_id=%s
            WHERE id=%s
        """
        cursor.execute(query, (email, dept_id, role_id, emp_id))
        conn.commit()

        cursor.close()
        conn.close()

        flash("Employee details updated successfully!", "success")
        return redirect(url_for('emplist'))
    
def add_employeelist(app):
    @app.route("/add_employee", methods=["POST"])
    @login_required
    def add_emp():
        conn = get_db_connection()
        cursor = conn.cursor()

        firstname = request.form['firstname']
        lastname = request.form['lastname']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        dept_id = request.form['dept_id']
        role_id = request.form['role_id']

        query = """
            INSERT INTO employee (firstname, lastname, username, email, password, dept_id, role_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (firstname, lastname, username, email, password, dept_id, role_id))
        
        conn.commit() 
        cursor.close()
        conn.close()
        return redirect(url_for('emplist'))
    
def add_client_list(app):    
    @app.route('/add_client', methods=['POST'])
    def add_client():
        conn = get_db_connection()
        cursor = conn.cursor()

        POC = request.form['POC']
        Company_Name = request.form['Company_Name']
        email = request.form['email']
        phone = request.form.get('phone', None)
        country = request.form.get('country', 'INDIA')

        query = """
            INSERT INTO Client_Details (POC, Company_Name, email, phone, country)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (POC, Company_Name, email, phone, country))
        
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('client_list'))
def add_client(app):    
    @app.route('/save_client', methods=['GET'])
    def save_client():
        return render_template('hr/add_client.html')
    
def list_client(app):    
    @app.route('/client_list')
    def client_list():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Client_Details ")
        clients = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('hr/client_list.html', clients=clients)

    
def delete_client(app):
    @app.route('/delete_client/<int:client_id>', methods=['GET'])
    def delete_client(client_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Client_Details WHERE client_id = %s", (client_id,))
        conn.commit()
        cursor.close()
        conn.close()
        flash("Client deleted successfully!", "success")
        return redirect(url_for('client_list'))

def update_get_client(app):

    @app.route('/update_client/<int:client_id>', methods=['GET'])
    def update_client(client_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Client_Details WHERE client_id = %s", (client_id,))
        client = cursor.fetchone()
        cursor.close()
        conn.close()

        if not client:
            flash("Client not found!", "danger")
            return redirect(url_for('client_list'))

        return render_template('hr/update_client.html', client=client)
    
def update_post_client(app):
    @app.route('/update_client/<int:client_id>', methods=['POST'])
    def save_update_client(client_id):
        POC = request.form['POC']
        Company_Name = request.form['Company_Name']
        email = request.form['email']
        phone = request.form.get('phone', None)
        country = request.form.get('country', 'INDIA')

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Client_Details
            SET POC=%s, Company_Name=%s, email=%s, phone=%s, country=%s
            WHERE client_id=%s
        """, (POC, Company_Name, email, phone, country, client_id))
        conn.commit()
        cursor.close()
        conn.close()

        flash("Client updated successfully!", "success")
        return redirect(url_for('client_list'))
    
  


