from app.models.db import get_db_connection

def historylist():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
       SELECT 
    h.id,
    CONCAT(e1.firstname, ' ', e1.lastname) AS assignto,
    CONCAT(e2.firstname, ' ', e2.lastname) AS assignby,
    d.dept_id,
    d.dept_name,
    h.duration,
    h.comments,
    h.problem_description,
    h.priority,
    h.start_date,
    h.end_date,
    h.status
FROM support_ticket h
INNER JOIN employee e1 ON h.assigned_to = e1.id
INNER JOIN employee e2 ON h.assigned_by = e2.id
LEFT JOIN department d ON h.dept_id = d.dept_id
WHERE h.status IN ('RESOLVED', 'CLOSED')
ORDER BY h.id;  
    """)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results


def assignlist():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            h.id,
            CONCAT(e1.firstname, ' ', e1.lastname) AS assignto,
            CONCAT(e2.firstname, ' ', e2.lastname) AS assignby,
            d.dept_id,
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
        WHERE (h.assigned_to IS NOT NULL and h.status = "OPEN")
    """)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results


def notassignlist():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            h.id,
            CONCAT(e1.firstname, ' ', e1.lastname) AS assignto,
            CONCAT(e2.firstname, ' ', e2.lastname) AS assignby,
            d.dept_id,
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
        WHERE (h.assigned_to IS NULL and h.status = "OPEN")
    """)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results


def get_ticket_by_id(ticket_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            h.*,
            d.dept_id,
            d.dept_name,
            CONCAT(e2.firstname, ' ', e2.lastname) AS assignby_name,
            h.assigned_to
        FROM support_ticket h
        LEFT JOIN department d ON h.dept_id = d.dept_id
        LEFT JOIN employee e2 ON h.assigned_by = e2.id
        WHERE h.id = %s
    """, (ticket_id,))
    ticket = cursor.fetchone()
    cursor.close()
    conn.close()
    return ticket


def get_employees_by_department(dept_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT id, CONCAT(firstname, ' ', lastname) AS name
        FROM employee
        WHERE dept_id = %s
    """, (dept_id,))
    employees = cursor.fetchall()
    cursor.close()
    conn.close()
    return employees


def update_ticket(ticket_id, data):
    """
    Update support_ticket including assigned_to.
    Expects:
        assigned_to, assigned_by, dept_id, duration,
        comments, problem_description, Priority (or priority), 
        Start_Date (or start_date), status
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    priority = data.get('Priority') or data.get('priority')
    start_date = data.get('Start_Date') or data.get('start_date')
    
    cursor.execute("""
        UPDATE support_ticket
        SET
            assigned_to = %s,
            assigned_by = %s,
            dept_id = %s,
            duration = %s,
            comments = %s,
            problem_description = %s,
            priority = %s,
            start_date = %s,
            status = %s
        WHERE id = %s
    """, (
        data.get('assigned_to'),
        data.get('assigned_by'),
        data.get('dept_id'),
        data.get('duration'),
        data.get('comments', ''),
        data.get('problem_description'),
        priority,
        start_date,
        data.get('status'),
        ticket_id
    ))
    conn.commit()
    cursor.close()
    conn.close()


def delete_ticket(ticket_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM support_ticket WHERE id = %s", (ticket_id,))
    conn.commit()
    cursor.close()
    conn.close()


def get_employees_by_department(dept_name):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT id, firstname, lastname
        FROM employee
        WHERE dept_id = (
            SELECT dept_id FROM department WHERE dept_name = %s
        )
    """, (dept_name,))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results
