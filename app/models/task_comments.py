import os
from werkzeug.utils import secure_filename
from app.models.db import get_db_connection

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'docx', 'sql'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def insert_task_comment(task_id, message, file, upload_folder):
    filename = None
    if file and file.filename != '' and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO Task_Comments (task_id, Message, Attachment)
        VALUES (%s, %s, %s)
    """, (task_id, message, filename))
    conn.commit()
    cur.close()
    conn.close()

    return filename
