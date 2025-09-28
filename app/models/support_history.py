from app.models.db import get_db_connection 


def historylist():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
     SELECT 
    sh.id,
    concat(e1.firstname,e1.lastname)  AS assignto,
    concat(e2.firstname,e2.lastname) AS assignby,
    d.dept_name,
    sh.duration,
    sh.comments,
    sh.problem_description,
    sh.priority,
    sh.start_date,
    sh.end_date,
    sh.status
FROM support_history sh
LEFT JOIN employee e1 ON sh.assigned_to = e1.id
LEFT JOIN employee e2 ON sh.assigned_by = e2.id
LEFT JOIN department d ON sh.dept_id = d.dept_id;
 
    """)
    historylist= cursor.fetchall()
    cursor.close()
    conn.close() 
    return historylist


def assignlist():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
     SELECT 
    h.id,
    concat(e1.firstname,e1.lastname)  AS assignto,
    concat(e2.firstname,e2.lastname) AS assignby,
    d.dept_name,
    h.duration,
    h.comments,
    h.problem_description,
    h.priority,
    h.start_date,
    h.end_date,
    h.status
FROM support_ticket h
LEFT JOIN employee e1 ON h.assigned_to = e1.id
LEFT JOIN employee e2 ON h.assigned_by = e2.id
LEFT JOIN department d ON h.dept_id = d.dept_id
where h.assigned_to is  not null;
   
 
    """)
    assignlist= cursor.fetchall()
    cursor.close()
    conn.close() 
    return assignlist

def notassignlist():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
     SELECT 
    h.id,
    concat(e1.firstname,e1.lastname)  AS assignto,
    concat(e2.firstname,e2.lastname) AS assignby,
    d.dept_name,
    h.duration,
    h.comments,
    h.problem_description,
    h.priority,
    h.start_date,
    h.end_date,
    h.status
FROM support_ticket h
LEFT JOIN employee e1 ON h.assigned_to = e1.id
LEFT JOIN employee e2 ON h.assigned_by = e2.id
LEFT JOIN department d ON h.dept_id = d.dept_id
where h.assigned_to is  null;
   
    """)
    notassignlist= cursor.fetchall()
    cursor.close()
    conn.close() 
    print(notassignlist)
    return notassignlist


