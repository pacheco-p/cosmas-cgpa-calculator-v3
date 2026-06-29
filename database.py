import sqlite3

# -----------------------------
# Database Connection
# -----------------------------
conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

# -----------------------------
# Initialize Database
# -----------------------------
def init_db():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS history(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        gpa REAL NOT NULL,
        cgpa REAL NOT NULL,
        total_cu INTEGER NOT NULL,
        total_qp REAL NOT NULL,
        semester_label TEXT,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Run automatic migration if using an older db file version
    try:
        cursor.execute("ALTER TABLE history ADD COLUMN semester_label TEXT;")
    except sqlite3.OperationalError:
        pass  # Column already exists

    conn.commit()

init_db()

# -----------------------------
# USER FUNCTIONS
# -----------------------------
def create_user(username, email, password):
    try:
        cursor.execute(
            """
            INSERT INTO users(username, email, password)
            VALUES(?,?,?)
            """,
            (username, email, password)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def get_user(username):
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    return cursor.fetchone()

def get_email(email):
    cursor.execute("SELECT * FROM users WHERE email=?", (email,))
    return cursor.fetchone()

# -----------------------------
# HISTORY FUNCTIONS
# -----------------------------
def save_history(username, gpa, cgpa, total_cu, total_qp, semester_label):
    cursor.execute(
        """
        INSERT INTO history(username, gpa, cgpa, total_cu, total_qp, semester_label)
        VALUES(?,?,?,?,?,?)
        """,
        (username, gpa, cgpa, total_cu, total_qp, semester_label)
    )
    conn.commit()

def get_history(username):
    cursor.execute(
        """
        SELECT id, gpa, cgpa, total_cu, total_qp, semester_label, date
        FROM history
        WHERE username=?
        ORDER BY date DESC
        """,
        (username,)
    )
    return cursor.fetchall()

def delete_history(record_id):
    cursor.execute("DELETE FROM history WHERE id=?", (record_id,))
    conn.commit()

def get_statistics(username):
    cursor.execute(
        """
        SELECT COUNT(*), MAX(cgpa), AVG(cgpa)
        FROM history
        WHERE username=?
        """,
        (username,)
    )
    return cursor.fetchone()
