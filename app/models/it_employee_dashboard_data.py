from app.models.db import get_db_connection
from datetime import datetime

# 1. Ticket Stats for Top Cards
def get_it_employee_ticket_stats(emp_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM support_ticket WHERE assigned_to = %s", (emp_id,))
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM support_ticket WHERE assigned_to = %s AND status = 'OPEN'", (emp_id,))
    pending = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM support_history WHERE assigned_to = %s AND status = 'RESOLVED'", (emp_id,))
    resolved = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM support_history WHERE assigned_to = %s AND status = 'CLOSED'", (emp_id,))
    completed = cursor.fetchone()[0]

    current_month = datetime.now().strftime('%Y-%m')
    cursor.execute("""
        SELECT COUNT(*) FROM support_ticket 
        WHERE assigned_to = %s AND DATE_FORMAT(created_at, '%%Y-%%m') = %s
    """, (emp_id, current_month))
    monthly = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return {
        'total_tickets': total,
        'pending_tickets': pending,
        'resolved_tickets': resolved,
        'completed_tickets': completed,
        'monthly_tickets': monthly
    }

# 2. Monthly Ticket Count for Line Chart
def get_monthly_ticket_counts_for_employee(emp_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DATE_FORMAT(created_at, '%Y-%m') AS month, COUNT(*) AS count
        FROM support_ticket
        WHERE assigned_to = %s
        GROUP BY month
        ORDER BY month
    """, (emp_id,))
    rows = cursor.fetchall()
    conn.close()

    months = [row[0] for row in rows]
    counts = [row[1] for row in rows]
    return months, counts

# 3. Pie Chart - Status Distribution (from both live and historical data)
def get_status_distribution_for_employee(emp_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT status, COUNT(*) FROM (
            SELECT status FROM support_ticket WHERE assigned_to = %s
            UNION ALL
            SELECT status FROM support_history WHERE assigned_to = %s
        ) AS all_tickets
        GROUP BY status
    """, (emp_id, emp_id))
    
    rows = cursor.fetchall()
    conn.close()
    status_counts = {row[0]: row[1] for row in rows}
    return status_counts

# 4. Recent Tickets (limit 5)
def get_recent_tickets_for_employee(emp_id, limit=5):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, problem_description, status, created_at 
        FROM support_ticket
        WHERE assigned_to = %s
        ORDER BY created_at DESC
        LIMIT %s
    """, (emp_id, limit))

    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    return [{
        'ticket_id': row[0],
        'problem_description': row[1],
        'status': row[2],
        'created_at': row[3]
    } for row in rows]



def get_employee_by_id(employee_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT id, firstname, email, dept_id, role_id
            FROM employee
            WHERE id = %s
        """
        cursor.execute(query, (employee_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result
    
def get_tickets_by_employee(employee_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
        SELECT 
    e1.id AS employee_id,
    e1.firstname,
    e1.lastname,
    e1.email,
    d.dept_name AS department,
    r.role_name AS role
FROM employee e1
LEFT JOIN department d ON e1.dept_id = d.dept_id
LEFT JOIN roles r ON e1.role_id = r.id
WHERE e1.id IN (
    SELECT st.assigned_to 
    FROM support_ticket st 
    WHERE st.assigned_by = %s
)
ORDER BY e1.firstname;
        """
        cursor.execute(query, (employee_id,))
        result = cursor.fetchall()
        print(2)
        print(result)
        cursor.close()
        conn.close()
        return result
