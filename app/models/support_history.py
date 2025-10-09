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
    Only updates fields that are provided (not None).
    Expects:
        assigned_to, assigned_by, dept_id, duration,
        comments (optional), problem_description (optional), 
        priority (optional), start_date (optional), status
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Handle both Priority/priority and Start_Date/start_date cases
    priority = data.get('Priority') or data.get('priority')
    start_date = data.get('Start_Date') or data.get('start_date')
    problem_description = data.get('problem_description')
    
    # Build dynamic UPDATE query to only update provided fields
    update_fields = []
    update_values = []
    
    # Always update these core assignment fields
    update_fields.append("assigned_to = %s")
    update_values.append(data.get('assigned_to'))
    
    update_fields.append("assigned_by = %s")
    update_values.append(data.get('assigned_by'))
    
    update_fields.append("dept_id = %s")
    update_values.append(data.get('dept_id'))
    
    update_fields.append("duration = %s")
    update_values.append(data.get('duration'))
    
    update_fields.append("status = %s")
    update_values.append(data.get('status'))
    
    # Only update optional fields if they are provided and not None
    if data.get('comments') is not None:
        update_fields.append("comments = %s")
        update_values.append(data.get('comments', ''))
    
    if problem_description is not None:
        update_fields.append("problem_description = %s")
        update_values.append(problem_description)
    
    if priority is not None:
        update_fields.append("priority = %s")
        update_values.append(priority)
    
    if start_date is not None:
        update_fields.append("start_date = %s")
        update_values.append(start_date)
    
    # Add ticket_id for WHERE clause
    update_values.append(ticket_id)
    
    # Construct final query
    query = f"""
        UPDATE support_ticket
        SET {', '.join(update_fields)}
        WHERE id = %s
    """
    
    print(f"Executing query: {query}")  # Debug log
    print(f"With values: {update_values}")  # Debug log
    
    cursor.execute(query, tuple(update_values))
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
