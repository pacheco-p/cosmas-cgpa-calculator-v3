import streamlit as st
import auth

def show():

    st.title("👤 My Profile")

    user = auth.get_user(st.session_state.username)

    full_name = st.text_input(
        "Full Name",
        value=user["full_name"] if user["full_name"] else ""
    )

    matric_number = st.text_input(
        "Matric Number",
        value=user["matric_number"] if user["matric_number"] else ""
    )

    department = st.text_input(
        "Department",
        value=user["department"] if user["department"] else ""
    )

    faculty = st.text_input(
        "Faculty",
        value=user["faculty"] if user["faculty"] else ""
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
        value=user["admission_year"] if user["admission_year"] else ""
    )

    if st.button("💾 Save Profile", use_container_width=True):

        auth.update_profile(
            st.session_state.username,
            full_name,
            matric_number,
            department,
            faculty,
            level,
            admission_year
        )

        st.success("Profile updated successfully!")

    st.divider()

    st.subheader("Profile Summary")

    st.write(f"**Username:** {user['username']}")
    st.write(f"**Email:** {user['email']}")
    st.write(f"**Full Name:** {full_name}")
    st.write(f"**Matric Number:** {matric_number}")
    st.write(f"**Department:** {department}")
    st.write(f"**Faculty:** {faculty}")
    st.write(f"**Level:** {level}")
    st.write(f"**Admission Year:** {admission_year}")
