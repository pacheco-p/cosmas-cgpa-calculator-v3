import streamlit as st
import database


def show():

    st.title("👤 Student Profile")

    username = st.session_state.username

    user = database.get_user(username)

    if user is None:
        st.error("User not found.")
        return

    st.write("Update your personal information below.")

    with st.form("profile_form"):

        full_name = st.text_input(
            "Full Name",
            value=user["full_name"] or ""
        )

        matric_number = st.text_input(
            "Matric Number",
            value=user["matric_number"] or ""
        )

        faculty = st.text_input(
            "Faculty",
            value=user["faculty"] or ""
        )

        department = st.text_input(
            "Department",
            value=user["department"] or ""
        )

        current_level = st.selectbox(
            "Current Level",
            [
                "100 Level",
                "200 Level",
                "300 Level",
                "400 Level",
                "500 Level",
                "600 Level"
            ],
            index=0 if not user["current_level"] else
            [
                "100 Level",
                "200 Level",
                "300 Level",
                "400 Level",
                "500 Level",
                "600 Level"
            ].index(user["current_level"])
        )

        admission_year = st.text_input(
            "Admission Year",
            value=user["admission_year"] or ""
        )

        save = st.form_submit_button(
            "💾 Save Profile",
            use_container_width=True
        )

        if save:

            database.update_profile(
                username,
                full_name,
                matric_number,
                department,
                faculty,
                current_level,
                admission_year
            )

            st.success("Profile updated successfully.")

    st.divider()

    st.subheader("Current Information")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Username:**", user["username"])
        st.write("**Full Name:**", user["full_name"] or "-")
        st.write("**Matric Number:**", user["matric_number"] or "-")

    with col2:
        st.write("**Faculty:**", user["faculty"] or "-")
        st.write("**Department:**", user["department"] or "-")
        st.write("**Current Level:**", user["current_level"] or "-")
        st.write("**Admission Year:**", user["admission_year"] or "-")
