import sqlite3

conn = sqlite3.connect("cgpa.db", check_same_thread=False)
conn.row_factory = sqlite3.Row
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
        admission_year=?
    WHERE username=?
    """, (
        full_name,
        matric_number,
        department,
        faculty,
        level,
        admission_year,
        username
    ))

    conn.commit()


def get_profile(username):
    cursor.execute(
        "SELECT * FROM users WHERE username=?",
        (username,)
    )
    return cursor.fetchone()


# ==========================
# RESULT FUNCTIONS
# ==========================

def save_result(username, session, semester, gpa, cgpa):

    cursor.execute("""
    INSERT INTO results(
        username,
        session,
        semester,
        gpa,
        cgpa
    )
    VALUES(?,?,?,?,?)
    """, (
        username,
        session,
        semester,
        gpa,
        cgpa
    ))

    conn.commit()


def get_results(username):

    cursor.execute("""
    SELECT *
    FROM results
    WHERE username=?
    ORDER BY id DESC
    """, (
        username,
    ))

    return cursor.fetchall()


def delete_result(result_id):

    cursor.execute(
        "DELETE FROM results WHERE id=?",
        (result_id,)
    )

    conn.commit()


def clear_results(username):

    cursor.execute(
        "DELETE FROM results WHERE username=?",
        (username,)
    )

    conn.commit()


def close_connection():
    conn.close()
