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
# COURSE FUNCTIONS
# ==========================================

def add_course(
    department,
    level,
    semester,
    course_code,
    course_title,
    credit_unit
):
    cursor.execute("""
    INSERT INTO courses
    (department,level,semester,course_code,course_title,credit_unit)
    VALUES(?,?,?,?,?,?)
    """,
    (
        department,
        level,
        semester,
        course_code,
        course_title,
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
    """,
    (
        department,
        level,
        semester
    ))

    return cursor.fetchall()
