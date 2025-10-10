from werkzeug.utils import secure_filename
from app.models.db import get_db_connection
import os
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'docx', 'sql'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
def insert_support_comment(supt_id, message, file, upload_folder):
    filename = None
    if file and file.filename != '' and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO Support_tkt_comments (Supt_id, Message, Attachment)
        VALUES (%s, %s, %s)
    """, (supt_id, message, filename))
    conn.commit()
    cur.close()
    conn.close()
    return filename



