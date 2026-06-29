import streamlit as st
import sqlite3
import bcrypt
import pandas as pd

# ----------------------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------------------
st.set_page_config(
    page_title="Cosmas CGPA Calculator",
    page_icon="🎓",
    layout="wide"
)

# ----------------------------------------------------------------
# CONSOLIDATED DATABASE LAYER (Old database.py)
# ----------------------------------------------------------------
conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

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
    try:
        cursor.execute("ALTER TABLE history ADD COLUMN semester_label TEXT;")
    except sqlite3.OperationalError:
        pass  
    conn.commit()

init_db()

def db_create_user(username, email, password):
    try:
        cursor.execute("INSERT INTO users(username, email, password) VALUES(?,?,?)", (username, email, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def db_get_user(username):
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
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
# CONSOLIDATED AUTHENTICATION LAYER (Old auth.py)
# ----------------------------------------------------------------
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

def run_registration(username, email, password):
    username = username.strip()
    email = email.strip().lower()
    if db_get_user(username):
        return False, "Username already exists."
    if db_get_email(email):
        return False, "Email already exists."
    hashed_password = hash_password(password)
    db_create_user(username, email, hashed_password)
    return True, "Account created successfully."

def run_login(username, password):
    user = db_get_user(username)
    if user is None:
        return False
    return verify_password(password, user[3])


# ----------------------------------------------------------------
# LAZY PAGES IMPORT (Safe from caching anomalies)
# ----------------------------------------------------------------
import dashboard
import calculator
import history
import profile
import settings

# Patch the remaining sub-modules temporarily so they hit our working DB functions
import sys
import types
mock_db = types.ModuleType('database')
mock_db.get_statistics = db_get_statistics
mock_db.get_history = db_get_history
mock_db.get_user = db_get_user
mock_db.save_history = db_save_history
mock_db.delete_history = db_delete_history
sys.modules['database'] = mock_db


# ----------------------------------------------------------------
# SESSION STATE SETUP
# ----------------------------------------------------------------
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
            st.title("🏛️ COSMAS AT SUG TOP SEAT")

        st.title("🎓 Cosmas CGPA Calculator")
        st.caption("Support • Pray • Canvass")

        login_tab, signup_tab = st.tabs(["🔑 Login", "📝 Create Account"])

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
            password = st.text_input("Password", type="password", key="signup_password")
            confirm = st.text_input("Confirm Password", type="password")

            if st.button("Create Account", use_container_width=True):
                if password != confirm:
                    st.error("Passwords do not match.")
                elif len(password) < 6:
                    st.warning("Password must be at least 6 characters.")
                else:
                    success, message = run_registration(username, email, password)
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
        ["🏠 Dashboard", "🎓 CGPA Calculator", "📊 History", "👤 Profile", "⚙️ Settings"]
    )

    st.sidebar.divider()

    if st.sidebar.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()

    # Routing Engine
    if page == "🏠 Dashboard":
        dashboard.show()
    elif page == "🎓 CGPA Calculator":
        calculator.show()
    elif page == "📊 History":
        history.show()
    elif page == "👤 Profile":
        profile.show()
    elif page == "⚙️ Settings":
        settings.show()
