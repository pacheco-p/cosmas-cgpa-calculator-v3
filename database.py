import sqlite3

conn = sqlite3.connect("cgpa.db", check_same_thread=False)
cursor = conn.cursor()

# ==========================
# USERS TABLE
# ==========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    email TEXT,
    password TEXT,
    full_name TEXT,
    matric_number TEXT,
    department TEXT,
    faculty TEXT,
    level TEXT,
    admission_year TEXT
)
""")

# ==========================
# RESULTS TABLE
# ==========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS results(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    session TEXT,
    semester TEXT,
    gpa REAL,
    cgpa REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()


# ==========================
# USER FUNCTIONS
# ==========================

def create_user(username, email, password):
    try:
        cursor.execute(
            """
            INSERT INTO users(username,email,password)
            VALUES(?,?,?)
            """,
            (username, email, password)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False


def get_user(username):
    cursor.execute(
        "SELECT * FROM users WHERE username=?",
        (username,)
    )
    return cursor.fetchone()


def update_profile(
    username,
    full_name,
    matric_number,
    department,
    faculty,
    level,
    admission_year
):
    cursor.execute("""
        UPDATE users
        SET
        full_name=?,
        matric_number=?,
        department=?,
        faculty=?,
        level=?,
