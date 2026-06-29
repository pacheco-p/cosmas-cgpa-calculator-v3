import streamlit as st
import database


def show():

    st.title("👤 My Profile")

    user = database.get_user(st.session_state.username)

    if not user:
        st.error("User not found.")
        return

    st.subheader("Update Your Profile")

    full_name = st.text_input(
        "Full Name",
        value=user["full_name"] or ""
    )

    matric_number = st.text_input(
        "Matric Number",
        value=user["matric_number"] or ""
    )

    department = st.text_input(
        "Department",
        value=user["department"] or ""
    )

    faculty = st.text_input(
        "Faculty",
        value=user["faculty"] or ""
    )

    level = st.selectbox(
        "Level",
        [
            "100 Level",
            "200 Level",
            "300 Level",
            "400 Level",
            "500 Level"
        ],
        index=0 if not user["level"] else [
            "100 Level",
            "200 Level",
            "300 Level",
            "400 Level",
            "500 Level"
        ].index(user["level"])
    )

    admission_year = st.text_input(
        "Admission Year",
        value=user["admission_year"] or ""
    )

    if st.button(
        "💾 Save Profile",
        use_container_width=True
    ):

        database.update_profile(
            st.session_state.username,
            full_name,
            matric_number,
            department,
            faculty,
            level,
            admission_year
        )

        st.success("Profile updated successfully.")
        st.rerun()

    st.divider()

    st.subheader("Current Information")

    st.write(f"**Username:** {user['username']}")
    st.write(f"**Email:** {user['email']}")
    st.write(f"**Full Name:** {user['full_name'] or 'Not Set'}")
    st.write(f"**Matric Number:** {user['matric_number'] or 'Not Set'}")
    st.write(f"**Department:** {user['department'] or 'Not Set'}")
    st.write(f"**Faculty:** {user['faculty'] or 'Not Set'}")
    st.write(f"**Level:** {user['level'] or 'Not Set'}")
    st.write(f"**Admission Year:** {user['admission_year'] or 'Not Set'}")
