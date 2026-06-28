import sqlite3

# ==========================================
# DATABASE CONNECTION
# ==========================================

conn = sqlite3.connect("cgpa.db", check_same_thread=False)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# ==========================================
# USERS TABLE
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,

    full_name TEXT,
    matric_number TEXT,
    department TEXT,
    faculty TEXT,
    level TEXT,
    admission_year TEXT
)
""")

# ==========================================
# RESULTS TABLE
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS results(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    session TEXT,
    semester TEXT,
    gpa REAL,
    cgpa REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# ==========================================
# COURSES TABLE
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS courses(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    department TEXT,
    level TEXT,
    semester TEXT,
    course_code TEXT,
    course_title TEXT,
    credit_unit INTEGER
)
""")

conn.commit()

# ==========================================
# USER FUNCTIONS
# ==========================================

def create_user(username, email, password):
    cursor.execute("""
    INSERT INTO users(username,email,password)
    VALUES(?,?,?)
    """, (username, email, password))
    conn.commit()


def get_user(username):
    cursor.execute("""
    SELECT *
    FROM users
    WHERE username=?
    """, (username,))
    return cursor.fetchone()


def get_email(email):
    cursor.execute("""
    SELECT *
    FROM users
    WHERE email=?
    """, (email,))
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
        admission_year=?
    WHERE username=?
    """,
