import streamlit as st
import auth
import dashboard
import calculator
import history
import profile

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="Cosmas CGPA Calculator",
    page_icon="🎓",
    layout="wide"
)

# =====================================
# SESSION STATE
# =====================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

# =====================================
# LOGIN / SIGNUP
# =====================================

if not st.session_state.logged_in:

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        st.title("🎓 Cosmas CGPA Calculator")
        st.caption("Calculate your GPA & CGPA with ease.")

        login_tab, signup_tab = st.tabs(
            ["🔑 Login", "📝 Create Account"]
        )

        # ---------------- LOGIN ----------------

        with login_tab:

            username = st.text_input(
                "Username",
                key="login_username"
            )

            password = st.text_input(
                "Password",
                type="password",
                key="login_password"
            )

            if st.button(
                "Login",
                use_container_width=True
            ):

                if auth.login(username, password):

                    st.session_state.logged_in = True
                    st.session_state.username = username

                    st.rerun()

                else:

                    st.error(
                        "Invalid username or password."
                    )

        # ---------------- SIGN UP ----------------

        with signup_tab:

            new_username = st.text_input(
                "Username",
                key="signup_username"
            )

            email = st.text_input(
                "Email",
                key="
