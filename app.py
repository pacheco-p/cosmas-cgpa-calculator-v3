import streamlit as st
import database as db
import dashboard
import calculator
import profile
import history

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
            email = st.text_input("Email Address")
            matric = st.text_input("Matric Number")
            dept = st.text_input("Department")
            level = st.selectbox("Current Level", ["100L", "200L", "300L", "400L", "500L"])
            
        submit = st.form_submit_button("Proceed")
        
        if submit:
            import sqlite3
            if auth_mode == "Register/Sign Up":
                if username and password and confirm_password and fullname:
                    # Validate that both password fields match exactly
                    if password != confirm_password:
                        st.error("Passwords do not match. Please verify your password entry.")
                    elif len(password) < 6:
                        st.warning("For safety, your password must be at least 6 characters long.")
                    else:
                        try:
                            conn = sqlite3.connect("users.db")
                            cursor = conn.cursor()
                            cursor.execute
