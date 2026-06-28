import streamlit as st
import auth
import dashboard
import calculator
import history
import profile

# =====================================
# PAGE CONFIGURATION
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
# LOGIN / SIGNUP PAGE
# =====================================

if not st.session_state.logged_in:

    left, center, right = st.columns([1,2,1])

    with center:

        st.title("🎓 Cosmas CGPA Calculator")
        st.caption("Calculate your GPA & CGPA with ease.")

        login_tab, signup_tab = st.tabs([
            "🔑 Login",
            "📝 Create Account"
        ])

        # ---------------- LOGIN ----------------

        with login_tab:

            login_username = st.text_input(
                "Username",
                key="login_username"
            )

            login_password = st.text_input(
                "Password",
                type="password",
                key="login_password"
            )

            if st.button(
                "Login",
                use_container_width=True
            ):

                if auth.login(
                    login_username,
                    login_password
                ):

                    st.session_state.logged_in = True
                    st.session_state.username = login_username

                    st.success("Login Successful!")
                    st.rerun()

                else:

                    st.error(
                        "Invalid username or password."
                    )

        # ---------------- SIGNUP ----------------

        with signup_tab:

            signup_username = st.text_input(
                "Username",
                key="signup_username"
            )

            signup_email = st.text_input(
                "Email",
                key="signup_email"
            )

            signup_password = st.text_input(
                "Password",
                type="password",
                key="signup_password"
            )

            confirm_password = st.text_input(
                "Confirm Password",
                type="password",
                key="signup_confirm"
            )

            if st.button(
                "Create Account",
                use_container_width=True
            ):

                if signup_password != confirm_password:

                    st.error(
                        "Passwords do not match."
                    )

                else:

                    success, message = auth.register(
                        signup_username,
                        signup_email,
                        signup_password
                    )

                    if success:

                        st.success(message)

                    else:

                        st.error(message)

# =====================================
# MAIN APPLICATION
# =====================================

else:

    st.sidebar.title("🎓 Cosmas CGPA")

    st.sidebar.success(
        f"Welcome, {st.session_state.username}"
    )

    page = st.sidebar.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "🎓 Calculator",
            "📊 History",
            "👤 Profile"
        ]
    )

    st.sidebar.divider()

    if st.sidebar.button(
        "🚪 Logout",
        use_container_width=True
    ):

        st.session_state.logged_in = False
        st.session_state.username = ""

        st.rerun()

    # =====================================
    # PAGE ROUTING
    # =====================================

    if page == "🏠 Dashboard":
        dashboard.show()

    elif page == "🎓 Calculator":
        calculator.show()

    elif page == "📊 History":
        history.show()

    elif page == "👤 Profile":
        profile.show()
