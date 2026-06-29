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
    current_level TEXT,
    admission_year TEXT
)
""")

# ==========================
# COURSES TABLE
# ==========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS courses(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    department TEXT NOT NULL,
    level TEXT NOT NULL,
    semester TEXT NOT NULL,
    course_code TEXT NOT NULL,
    credit_unit INTEGER NOT NULL
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

# ======================================================
# USER FUNCTIONS
# ======================================================

def create_user(username, email, password):
    try:
        cursor.execute("""
        INSERT INTO users(username,email,password)
        VALUES(?,?,?)
        """, (username, email, password))
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
    current_level,
    admission_year
):

    cursor.execute("""
    UPDATE users
    SET
        full_name=?,
        matric_number=?,
        department=?,
        faculty=?,
        current_level=?,
        admission_year=?
    WHERE username=?
    """, (
        full_name,
        matric_number,
        department,
        faculty,
        current_level,
        admission_year,
        username
    ))

    conn.commit()

# ======================================================
# COURSE FUNCTIONS
# ======================================================

def add_course(
    department,
    level,
    semester,
    course_code,
    credit_unit
):

    cursor.execute("""
    INSERT INTO courses(
        department,
        level,
        semester,
        course_code,
        credit_unit
    )
    VALUES(?,?,?,?,?)
    """, (
        department,
        level,
        semester,
        course_code.upper(),
        credit_unit
    ))

    conn.commit()


def get_courses(
    department,
    level,
    semester
):

    cursor.execute("""
    SELECT *
    FROM courses
    WHERE department=?
    AND level=?
    AND semester=?
    ORDER BY course_code
    """, (
        department,
        level,
        semester
    ))

    return cursor.fetchall()


def delete_course(course_id):

    cursor.execute(
        "DELETE FROM courses WHERE id=?",
        (course_id,)
    )

    conn.commit()

# ======================================================
# RESULT FUNCTIONS
# ======================================================

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
    """, (
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
    """, (username,))

    return cursor.fetchall()


def get_previous_result(username):

    cursor.execute("""
    SELECT *
    FROM results
    WHERE username=?
    ORDER BY created_at DESC
    LIMIT 1
    """, (username,))

    return cursor.fetchone()


def delete_result(result_id):

    cursor.execute(
        "DELETE FROM results WHERE id=?",
        (result_id,)
    )

    conn.commit()
