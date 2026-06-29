import streamlit as st
import database as db
import dashboard
import calculator
import profile
import history
import sqlite3

# Initialize App Configurations
st.set_page_config(page_title="Cosmas CGPA Engine", page_icon="🎓", layout="wide")
db.init_db()

# Session State Setup
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = None

# If not logged in, show the Auth Portal (Login / Registration)
if not st.session_state.authenticated:
    
    # 1. COSMAS BANNER HEADLINER ON AUTHENTICATION PAGE
    try:
        st.image("assets/cosmas_banner.png", use_container_width=True)
    except:
        st.markdown("""
        <div style="background: linear-gradient(90deg, #1e3a8a 0%, #0f172a 100%); padding: 30px; border-radius: 10px; text-align: center; margin-bottom: 20px;">
            <h1 style="color: white; margin: 0; font-family: sans-serif; letter-spacing: 2px;">COSMAS AT SUG TOP SEAT</h1>
            <p style="color: #cbd5e1; margin: 5px 0 0 0; font-family: sans-serif;">Support • Pray • Canvass</p>
        </div>
        """, unsafe_allow_html=True)

    st.title("Welcome to Cosmas CGPA Workspace")
    
    # Initialize the radio index state to control automatic toggling
    if "auth_mode_index" not in st.session_state:
        st.session_state.auth_mode_index = 0

    auth_mode = st.radio(
        "Choose Action", 
        ["Login", "Register/Sign Up"], 
        index=st.session_state.auth_mode_index,
        key="auth_mode_selector"
    )
    
    with st.form("auth_form", clear_on_submit=False):
        username = st.text_input("Username").strip().lower()
        password = st.text_input("Password", type="password")
        
        if auth_mode == "Register/Sign Up":
            confirm_password = st.text_input("Confirm Password", type="password")
            fullname = st.text_input("Full Name")
            email = st.text_input("Email Address").strip()
            matric = st.text_input("Matric Number").strip().upper()
            dept = st.text_input("Department")
            level = st.selectbox("Current Level", ["100L", "200L", "300L", "400L", "500L"])
            
        submit = st.form_submit_button("Proceed")
        
        if submit:
            if auth_mode == "Register/Sign Up":
                if username and password and confirm_password and fullname and dept:
                    # Validate that both password fields match exactly
                    if password != confirm_password:
                        st.error("Passwords do not match. Please verify your password entry.")
                    elif len(password) < 6:
                        st.warning("For safety, your password must be at least 6 characters long.")
                    else:
                        try:
                            # AUTOMATIC CAPITALIZATION APPLIED HERE
                            formatted_fullname = fullname.strip().title()  # e.g., "John Doe"
                            formatted_dept = dept.strip().upper()          # e.g., "INDUSTRIAL CHEMISTRY"
                            
                            conn = sqlite3.connect("users.db")
                            cursor = conn.cursor()
                            cursor.execute("INSERT INTO users VALUES (?,?,?,?,?,?,?)", 
                                           (username, password, formatted_fullname, email, matric, formatted_dept, level))
                            conn.commit()
                            conn.close()
                            
                            # IMMEDIATELY FLIP TRACKER TO LOGIN MODE INDEX (0) AND RERUN
                            st.session_state.auth_mode_index = 0
                            st.success("Registration successful! Redirecting you to login...")
                            st.rerun()
                        except sqlite3.IntegrityError:
                            st.error("Username already taken.")
                        except Exception as e:
                            st.error(f"An unexpected error occurred: {e}")
                else:
                    st.error("Please fill out all required fields.")
            else:
                # Login Processing
                conn = sqlite3.connect("users.db")
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
                user_match = cursor.fetchone()
                conn.close()
                if user_match:
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.rerun()
                else:
                    st.error("Invalid Username or Password Credentials.")
else:
    # Sidebar Navigation Wrapper
    st.sidebar.title("Navigation")
    menu_selection = st.sidebar.radio("Go to:", ["Dashboard", "CGPA Calculator", "History Log", "My Profile"])
    
    st.sidebar.divider()
    if st.sidebar.button("Logout", type="primary", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.username = None
        if "returning_user" in st.session_state:
            del st.session_state.returning_user
        # Reset auth selector position state
        st.session_state.auth_mode_index = 0
        st.rerun()

    # Route Content Contexts
    if menu_selection == "Dashboard":
        dashboard.show(db.get_statistics, db.get_user_profile)
    elif menu_selection == "CGPA Calculator":
        calculator.show(db.get_history, db.save_history, db.get_user_profile)
    elif menu_selection == "History Log":
        history.show(db.get_history, db.delete_history)
    elif menu_selection == "My Profile":
        profile.show(db.get_user_profile, db.update_user_profile)
