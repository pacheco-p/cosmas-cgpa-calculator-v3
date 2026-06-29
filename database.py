import sqlite3

# ==========================
# DATABASE CONNECTION
# ==========================

conn = sqlite3.connect("cgpa.db", check_same_thread=False)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# ==========================
# USERS TABLE
# ==========================

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

# ==========================
# RESULTS TABLE
# ==========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS results(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    academic_session TEXT NOT NULL,
    level TEXT NOT NULL,
    semester TEXT NOT NULL,
    gpa REAL NOT NULL,
    cgpa REAL NOT NULL,
    total_credit_units INTEGER NOT NULL,
    total_quality_points REAL NOT NULL,
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
    """,(
        full_name,
        matric_number,
        department,
        faculty,
        level,
        admission_year,
        username
    ))

    conn.commit()

# ==========================
# RESULT FUNCTIONS
# ==========================

def save_result(
    username,
    academic_session,
    level,
    semester,
    gpa,
    cgpa,
    total_credit_units,
    total_quality_points
):

    cursor.execute("""
    INSERT INTO results(
        username,
        academic_session,
        level,
        semester,
        gpa,
        cgpa,
        total_credit_units,
        total_quality_points
    )
    VALUES(?,?,?,?,?,?,?,?)
    """,(
        username,
        academic_session,
        level,
        semester,
        gpa,
        cgpa,
        total_credit_units,
        total_quality_points
    ))

    conn.commit()


def get_results(username):

    cursor.execute("""
    SELECT *
    FROM results
    WHERE username=?
    ORDER BY created_at DESC
    """,(username,))

    return cursor.fetchall()


def delete_result(result_id):

    cursor.execute(
        "DELETE FROM results WHERE id=?",
        (result_id,)
    )

    conn.commit()


def get_previous_totals(username):

    cursor.execute("""
    SELECT
        total_credit_units,
        total_quality_points
    FROM results
    WHERE username=?
    ORDER BY created_at DESC
    LIMIT 1
    """,(username,))

    return cursor.fetchone()
