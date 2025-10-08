from app.models.db import get_db_connection

def get_total_tickets():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM support_ticket")
    total = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return total

def get_open_tickets():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM support_ticket WHERE status = 'OPEN'")
    total = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return total

def get_resolved_tickets():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM support_ticket WHERE status = 'RESOLVED'")
    total = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return total

def get_closed_tickets():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM support_ticket WHERE status = 'CLOSED'")
    total = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return total

def get_unassigned_tickets():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM support_ticket WHERE assigned_to IS NULL")
    total = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return total
def get_monthly_ticket_counts():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DATE_FORMAT(created_at, '%Y-%m') AS month, COUNT(*) AS ticket_count
        FROM support_ticket
        GROUP BY month
        ORDER BY month
    """)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    months = [row[0] for row in rows]
    ticket_counts = [row[1] for row in rows]
    return months, ticket_counts


def get_recent_tickets(limit=5):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, problem_description, status, created_at 
        FROM support_ticket
        ORDER BY created_at DESC
        LIMIT %s
    """, (limit,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    
    tickets = []
    for row in rows:
        tickets.append({
            'ticket_id': row[0],
            'problem_description': row[1],
            'status': row[2],
            'created_at': row[3]
        })
    return tickets
