import sqlite3

# ------------------------------------
# Database Connection
# ------------------------------------
conn = sqlite3.connect(
    "users.db",
    check_same_thread=False
)

cursor = conn.cursor()


# ------------------------------------
# Initialize Database
# ------------------------------------
def init_db():

    # ---------------- Users ----------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    # ---------------- History ----------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS history(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        session TEXT NOT NULL,
        semester TEXT NOT NULL,
        gpa REAL NOT NULL,
        cgpa REAL NOT NULL,
        total_cu INTEGER NOT NULL,
        total_qp REAL NOT NULL,
        classification TEXT NOT NULL,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # ---------------- Courses ----------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS courses(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        history_id INTEGER NOT NULL,
        course_code TEXT NOT NULL,
        credit_unit INTEGER NOT NULL,
        grade TEXT NOT NULL,
        grade_point INTEGER NOT NULL,
        quality_point REAL NOT NULL,
        FOREIGN KEY(history_id)
            REFERENCES history(id)
            ON DELETE CASCADE
    )
    """)

    conn.commit()


init_db()


# ------------------------------------
# USER FUNCTIONS
# ------------------------------------
def create_user(username, email, password):

    try:

        cursor.execute(
            """
            INSERT INTO users(
                username,
                email,
                password
            )
            VALUES(?,?,?)
            """,
            (
                username,
                email,
                password
            )
        )

        conn.commit()

        return True

    except sqlite3.IntegrityError:

        return False


def get_user(username):

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE username=?
        """,
        (username,)
    )

    return cursor.fetchone()


def get_email(email):

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE email=?
        """,
        (email,)
    )

    return cursor.fetchone()


# ------------------------------------
# HISTORY FUNCTIONS
# ------------------------------------
def save_history(
    username,
    session,
    semester,
    gpa,
    cgpa,
    total_cu,
    total_qp,
    classification
):

    cursor.execute(
        """
        INSERT INTO history(
            username,
            session,
            semester,
            gpa,
            cgpa,
            total_cu,
            total_qp,
            classification
        )
        VALUES(?,?,?,?,?,?,?,?)
        """,
        (
            username,
            session,
            semester,
            gpa,
            cgpa,
            total_cu,
            total_qp,
            classification
        )
    )

    conn.commit()

    return cursor.lastrowid
# ------------------------------------
# COURSE FUNCTIONS
# ------------------------------------
def save_courses(history_id, courses):

    for course in courses:

        cursor.execute(
            """
            INSERT INTO courses(
                history_id,
                course_code,
                credit_unit,
                grade,
                grade_point,
                quality_point
            )
            VALUES(?,?,?,?,?,?)
            """,
            (
                history_id,
                course["Course"],
                course["Credit Units"],
                course["Grade"],
                course["GP"],
                course["Quality Points"]
            )
        )

    conn.commit()


def get_courses(history_id):

    cursor.execute(
        """
        SELECT
            course_code,
            credit_unit,
            grade,
            grade_point,
            quality_point
        FROM courses
        WHERE history_id=?
        ORDER BY course_code
        """,
        (history_id,)
    )

    return cursor.fetchall()


# ------------------------------------
# HISTORY FUNCTIONS
# ------------------------------------
def get_history(username):

    cursor.execute(
        """
        SELECT
            id,
            session,
            semester,
            gpa,
            cgpa,
            total_cu,
            total_qp,
            classification,
            date
        FROM history
        WHERE username=?
        ORDER BY date DESC
        """,
        (username,)
    )

    return cursor.fetchall()


def delete_courses(history_id):

    cursor.execute(
        """
        DELETE FROM courses
        WHERE history_id=?
        """,
        (history_id,)
    )

    conn.commit()


def delete_history(record_id):

    delete_courses(record_id)

    cursor.execute(
        """
        DELETE FROM history
        WHERE id=?
        """,
        (record_id,)
    )

    conn.commit()


def get_statistics(username):

    cursor.execute(
        """
        SELECT
            COUNT(*),
            MAX(cgpa),
            AVG(cgpa)
        FROM history
        WHERE username=?
        """,
        (username,)
    )

    return cursor.fetchone()


# ------------------------------------
# CLOSE CONNECTION
# ------------------------------------
def close_connection():

    conn.close()