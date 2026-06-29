import sqlite3

def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    # Users table matching automatic capitalization expectations
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT,
            fullname TEXT,
            email TEXT,
            matric_no TEXT,
            department TEXT,
            current_level TEXT
        )
    """)
    # History tracking table for CGPA progress and metrics
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            gpa REAL,
            cgpa REAL,
            total_units INTEGER,
            quality_points REAL,
            semester_label TEXT,
            date_saved TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def get_user_profile(username):
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None

def update_user_profile(username, fullname, email, matric_no, department, current_level):
    try:
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        
        # Keep formatting professional and consistent during updates
        formatted_fullname = fullname.strip().title()
        formatted_dept = department.strip().upper()
        formatted_matric = matric_no.strip().upper()
        
        cursor.execute("""
            UPDATE users 
            SET fullname = ?, email = ?, matric_no = ?, department = ?, current_level = ? 
            WHERE username = ?
        """, (formatted_fullname, email.strip(), formatted_matric, formatted_dept, current_level, username))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Database Error: {e}")
        return False

def get_statistics(username):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*), MAX(cgpa), AVG(cgpa) 
        FROM history 
        WHERE username = ?
    """, (username,))
    stats = cursor.fetchone()
    conn.close()
    if stats and stats[0] > 0:
        return stats[0], stats[1] if stats[1] else 0.0, stats[2] if stats[2] else 0.0
    return 0, 0.0, 0.0

def save_history(username, gpa, cgpa, total_units, quality_points, semester_label):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO history (username, gpa, cgpa, total_units, quality_points, semester_label)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (username, gpa, cgpa, total_units, quality_points, semester_label.strip()))
    conn.commit()
    conn.close()

def get_history(username):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    # Pushes descending logs so dashboard snapshot captures recent logs first
    cursor.execute("""
        SELECT id, gpa, cgpa, total_units, quality_points, semester_label, date_saved 
        FROM history WHERE username = ? ORDER BY date_saved DESC
    """, (username,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_history(record_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM history WHERE id = ?", (record_id,))
    conn.commit()
    conn.close()
