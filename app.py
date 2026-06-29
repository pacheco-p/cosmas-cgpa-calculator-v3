import streamlit as st
import sqlite3
import bcrypt
import pandas as pd

# ----------------------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------------------
st.set_page_config(
    page_title="Cosmas CGPA Calculator",
    layout="wide"
)

# ----------------------------------------------------------------
# CONSOLIDATED DATABASE LAYER
# ----------------------------------------------------------------
conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

def init_db():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        fullname TEXT,
        matric_no TEXT,
        department TEXT,
        current_level TEXT
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
    columns = [col[1] for col in cursor.execute("PRAGMA table_info(users);").fetchall()]
    if "fullname" not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN fullname TEXT;")
        cursor.execute("ALTER TABLE users ADD COLUMN matric_no TEXT;")
        cursor.execute("ALTER TABLE users ADD COLUMN department TEXT;")
        cursor.execute("ALTER TABLE users ADD COLUMN current_level TEXT;")
    conn.commit()

init_db()

def db_create_user(username, email, password, fullname, matric_no, department, current_level):
    try:
        cursor.execute(
            "INSERT INTO users(username, email, password, fullname, matric_no, department, current_level) VALUES(?,?,?,?,?,?,?)", 
            (username, email, password, fullname, matric_no, department, current_level)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def db_get_user(username):
    cursor.execute("SELECT id, username, email, password, fullname, matric_no, department, current_level FROM users WHERE username=?", (username,))
    return cursor.fetchone()

def db_get_email(email):
    cursor.execute("SELECT * FROM users WHERE email=?", (email,))
    return cursor.fetchone()

def db_save_history(username, gpa, cgpa, total_cu, total_qp, semester_label):
    cursor.execute(
        "INSERT INTO history(username, gpa, cgpa, total_cu, total_qp, semester_label) VALUES(?,?,?,?,?,?)",
        (username, gpa, cgpa, total_cu, total_qp, semester_label)
    )
    conn.commit()

def db_get_history(username):
    cursor.execute("SELECT id, gpa, cgpa, total_cu, total_qp, semester_label, date FROM history WHERE username=? ORDER BY date DESC", (username,))
    return cursor.fetchall()

def db_delete_history(record_id):
    cursor.execute("DELETE FROM history WHERE id=?", (record_id,))
    conn.commit()

def db_get_statistics(username):
    cursor.execute("SELECT COUNT(*), MAX(cgpa), AVG(cgpa) FROM history WHERE username=?", (username,))
    return cursor.fetchone()


# ----------------------------------------------------------------
# CONSOLIDATED AUTHENTICATION LAYER
# ----------------------------------------------------------------
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

def run_registration(username, email, password, fullname, matric_no, department, current_level):
    username = username.strip()
    email = email.strip().lower()
    if db_get_user(username):
        return False, "Username already exists."
    if db_get_email(email):
        return False, "Email already exists."
    hashed_password = hash_password(password)
    db_create_user(username, email, hashed_password, fullname, matric_no, department, current_level)
    return True, "Account created successfully."

def run_login(username, password):
    user = db_get_user(username)
    if user is None:
        return False
    return verify_password(password, user[3])


# ----------------------------------------------------------------
# APP PAGES IMPORTS
# ----------------------------------------------------------------
import dashboard
import calculator
import history
import profile
import settings

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# ----------------------------------------------------------------
# UI CONTROLLER
# ----------------------------------------------------------------
if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        try:
            st.image("assets/cosmas_banner.png", use_container_width=True)
        except:
            st.title("COSMAS AT SUG TOP SEAT")

        st.title("Cosmas CGPA Calculator")
        st.caption("Support | Pray | Canvass")

        login_tab, signup_tab = st.tabs(["Login", "Create Account"])

        with login_tab:
            username = st.text_input("Username", key="login_username")
            password = st.text_input("Password", type="password", key="login_password")

            if st.button("Login", use_container_width=True):
                if run_login(username, password):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.success("Login Successful!")
                    st.rerun()
                else:
                    st.error("Invalid Username or Password.")

        with signup_tab:
            username = st.text_input("Choose Username", key="signup_username")
            email = st.text_input("Email Address")
            fullname = st.text_input("Full Name (Surname First)")
            matric_no = st.text_input("Matric Number")
            department = st.text_input("Department")
            current_level = st.selectbox("Current Level", ["100L", "200L", "300L", "400L", "500L"])
            password = st.text_input("Password", type="password", key="signup_password")
            confirm = st.text_input("Confirm Password", type="password")

            if st.button("Create Account", use_container_width=True):
                if password != confirm:
                    st.error("Passwords do not match.")
                elif len(password) < 6:
                    st.warning("Password must be at least 6 characters.")
                elif not fullname or not matric_no or not department:
                    st.warning("Please fill out all academic information fields.")
                else:
                    success, message = run_registration(username, email, password, fullname, matric_no, department, current_level)
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
else:
    try:
        st.sidebar.image("assets/cosmas_banner.png", use_container_width=True)
    except:
        pass

    st.sidebar.success(f"Welcome, {st.session_state.username}")

    page = st.sidebar.radio(
        "Navigation",
        ["Dashboard", "CGPA Calculator", "History", "Profile", "Settings"]
    )

    st.sidebar.divider()

    if st.sidebar.button("Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()

    if page == "Dashboard":
        dashboard.show(db_get_statistics, db_get_user)
    elif page == "CGPA Calculator":
        calculator.show(db_get_history, db_save_history, db_get_user)
    elif page == "History":
        history.show(db_get_history, db_delete_history)
    elif page == "Profile":
        profile.show(db_get_user)
    elif page == "Settings":
        settings.show()
