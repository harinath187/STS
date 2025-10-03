from app.models.db import get_db_connection

def get_user_by_credentials(username, password):
    conn = get_db_connection()
    
    if not conn:
        print("No database connection available.")
        return None

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT employee.*, department.dept_name as dep_name
            FROM employee 
            JOIN department ON employee.dept_id = department.dept_id 
            WHERE employee.username = %s AND employee.password = %s
        """, (username, password))
        
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        
        return user
    
    except Error as e:
        print(f"Error fetching user: {e}")
        if conn.is_connected():
            conn.close()
        return None


if __name__ == "__main__":
    user = get_user_by_credentials('testuser', 'testpassword')
    if user:
        print(f"User found: {user}")
    else:
        print("User not found.")
