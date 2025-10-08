from app.models.db import get_db_connection 
def employeelist():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
    SELECT  
    e.id,  
    e.firstname,  
    e.lastname,
    e.email,
    e.username,
    d.dept_name,  
    r.role_name  
FROM employee e
INNER JOIN department d ON e.dept_id = d.dept_id
INNER JOIN roles r ON e.role_id = r.id;
    """)
    emplist= cursor.fetchall()
    cursor.close()
    conn.close() 
    print(emplist)
    return emplist

def departmentlist():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
    SELECT dept_id,dept_name FROM department;
    """)
    deplist= cursor.fetchall()
    cursor.close()
    conn.close() 
    print("dept_list")
    print(deplist)
    return deplist
def roleslist():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
   select id,role_name,dept_id from roles;
    """)
    rolelist= cursor.fetchall()
    cursor.close()
    conn.close() 
    print(rolelist)
    return rolelist









    