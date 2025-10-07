from app.models.db import get_db_connection

def get_client_name():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    select * from Client_Details""")
    client = cursor.fetchall()
    print("client db ..................",client)
    cursor.close()
    conn.close()
    return client