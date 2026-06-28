import streamlit as st
import sqlite3

conn = sqlite3.connect("cgpa.db", check_same_thread=False)
cursor = conn.cursor()


def show():

    st.title("👤 My Profile")

    username = st.session_state.username

    cursor.execute("""
        SELECT
            username,
            email,
            full_name,
            matric_number,
            department,
            faculty,
            level,
            admission_year
        FROM users
        WHERE username=?
    """, (username,))

    user = cursor.fetchone()

    if not user:
        st.error("User not found.")
        return

    username, email, full_name, matric_number, department, faculty, level, admission_year = user

    st.subheader("Student Information")

    full_name = st.text_input(
        "Full Name",
        value=full_name if full_name else ""
    )

    matric_number = st.text_input(
        "Matric Number",
        value=matric_number if matric_number else ""
    )

    department = st.text_input(
        "Department",
        value=department if department else ""
    )

    faculty = st.text_input(
        "Faculty",
        value=faculty if faculty else ""
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
        index=[
            "100 Level",
            "200 Level",
            "300 Level",
            "400 Level",
            "500 Level"
        ].index(level) if level in [
            "100 Level",
            "200 Level",
            "300 Level",
            "400 Level",
            "500 Level"
        ] else 0
    )

    admission_year = st.text_input(
        "Admission Year",
        value=admission_year if admission_year else ""
    )

    st.text_input(
        "Email",
        value=email,
        disabled=True
    )

    st.text_input(
        "Username",
        value=username,
        disabled=True
    )

    if st.button("💾 Save Profile", use_container_width=True):

        cursor.execute("""
            UPDATE users
            SET
                full_name=?,
                matric_number=?,
                department=?,
                faculty=?,
                level=?,
                admission_year=?
            WHERE username=?
        """, (
            full_name,
            matric_number,
            department,
            faculty,
            level,
            admission_year,
            username
        ))

        conn.commit()

        st.success("Profile updated successfully!")
