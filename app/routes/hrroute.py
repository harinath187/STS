from flask import render_template, request, redirect, url_for, flash
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
        return render_template("hr/list_of_employees.html", employeelist=listitem,dept_list=department,role=roles)

def addemployee(app):
    @app.route("/addemployee") 
    @login_required 
    def add_emplist():
        department=departmentlist()
        roles=roleslist()
        return render_template("hr/Addemployee.html",dept_list=department,role=roles)

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
