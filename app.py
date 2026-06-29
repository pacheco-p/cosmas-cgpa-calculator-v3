import streamlit as st
import auth
import dashboard
import calculator
import history
import profile

# ==========================
# PAGE CONFIG
# ==========================

st.set_page_config(
    page_title="Cosmas CGPA Calculator",
    page_icon="🎓",
    layout="wide"
)

# ==========================
# SESSION STATE
# ==========================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

# ==========================
# LOGIN / SIGNUP
# ==========================

if not st.session_state.logged_in:

    st.title("🎓 Cosmas CGPA Calculator")
    st.caption("Calculate your GPA & CGPA easily")

    login_tab, signup_tab = st.tabs(
        ["🔑 Login", "📝 Sign Up"]
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
            key="signup_email"
        )

        new_password = st.text_input(
            "Password",
            type="password",
            key="signup_password"
        )

        confirm = st.text_input(
            "Confirm Password",
            type="password",
            key="signup_confirm"
        )

        if st.button(
            "Create Account",
            use_container_width=True
        ):

            if new_password != confirm:

                st.error("Passwords do not match.")

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

# ==========================
# MAIN APP
# ==========================

else:

    st.sidebar.title("🎓 Cosmas CGPA")

    st.sidebar.success(
        f"Welcome {st.session_state.username}"
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

    if page == "🏠 Dashboard":
        dashboard.show()

    elif page == "🎓 Calculator":
        calculator.show()

    elif page == "📊 History":
        history.show()

    elif page == "👤 Profile":
        profile.show()
