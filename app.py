import streamlit as st
import auth
import dashboard
import calculator
import history
import profile
import admin

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="EKSU Student CGPA Calculator",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================
# SESSION STATE
# =====================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

# =====================================
# LOGIN / REGISTER
# =====================================

if not st.session_state.logged_in:

    left, center, right = st.columns([1, 2, 1])

    with center:

        st.markdown(
            """
            # 🎓 EKSU Student CGPA Calculator

            ### An Independent GPA & CGPA Calculator for EKSU Students
            """
        )

        st.info(
            "Developed by COSMAS and His Team"
        )

        login_tab, register_tab = st.tabs(
            [
                "🔐 Login",
                "📝 Create Account"
            ]
        )

        # ---------------- LOGIN ----------------

        with login_tab:

            username = st.text_input(
                "Username"
            )

            password = st.text_input(
                "Password",
                type="password"
            )

            if st.button(
                "Login",
                use_container_width=True
            ):

                if auth.login(username, password):

                    st.session_state.logged_in = True
                    st.session_state.username = username

                    st.success("Login Successful")

                    st.rerun()

                else:

                    st.error(
                        "Invalid Username or Password."
                    )

        # ---------------- REGISTER ----------------

        with register_tab:

            new_username = st.text_input(
                "Username",
                key="reg_user"
            )

            email = st.text_input(
                "Email",
                key="reg_email"
            )

            new_password = st.text_input(
                "Password",
                type="password",
                key="reg_pass"
            )

            confirm = st.text_input(
                "Confirm Password",
                type="password",
                key="reg_confirm"
            )

            if st.button(
                "Create Account",
                use_container_width=True
            ):

                if new_password != confirm:

                    st.error(
                        "Passwords do not match."
                    )

                else:

                    success, message = auth.register(
                        new_username,
                        email,
                        new_password
                    )

                    if success:

                        st.success(message)

                    else:

                        st.error(message)

        st.divider()

        st.caption(
            "This application is an independent student project and is not affiliated with or endorsed by Ekiti State University."
        )

# =====================================
# MAIN APP
# =====================================

else:

    st.sidebar.title("🎓 EKSU CGPA")

    st.sidebar.success(
        f"Welcome, {st.session_state.username}"
    )

    page = st.sidebar.radio(
        "Navigation",
        [
            "Dashboard",
            "Calculator",
            "History",
            "Profile",
            "Admin"
        ]
    )

    st.sidebar.divider()

    if st.sidebar.button("🚪 Logout"):

        st.session_state.logged_in = False
        st.session_state.username = ""

        st.rerun()

    # =============================
    # PAGES
    # =============================

    if page == "Dashboard":
        dashboard.show()

    elif page == "Calculator":
        calculator.show()

    elif page == "History":
        history.show()

    elif page == "Profile":
        profile.show()

    elif page == "Admin":
        admin.show()
