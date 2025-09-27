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

