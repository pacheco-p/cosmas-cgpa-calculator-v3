import streamlit as st
import pandas as pd
import database


def show():

    st.title("🎓 CGPA Calculator")

    user = database.get_user(st.session_state.username)

    if not user:
        st.error("User not found.")
        return

    # ==========================
    # STUDENT INFORMATION
    # ==========================

    st.subheader("Student Information")

    col1, col2 = st.columns(2)

    with col1:
        st.write(f"**Name:** {user['full_name'] or 'Not Set'}")
        st.write(f"**Matric Number:** {user['matric_number'] or 'Not Set'}")
        st.write(f"**Department:** {user['department'] or 'Not Set'}")

    with col2:
        st.write(f"**Faculty:** {user['faculty'] or 'Not Set'}")
        st.write(f"**Level:** {user['level'] or 'Not Set'}")

    st.divider()

    # ==========================
    # SESSION DETAILS
    # ==========================

    session = st.text_input(
        "Academic Session",
        "2025/2026"
    )

    semester = st.selectbox(
        "Semester",
        [
            "First Semester",
            "Second Semester"
        ]
    )

    st.divider()

    # ==========================
    # GRADING SYSTEM
    # ==========================

    grades = {
        "A": 5,
        "B": 4,
        "C": 3,
        "D": 2,
        "E": 1,
        "F": 0
    }

    if "courses" not in st.session_state:
        st.session_state.courses = []

    st.subheader("Add Course")

    code = st.text_input("Course Code")

    title = st.text_input("Course Title")

    credit = st.number_input(
        "Credit Unit",
        min_value=1,
        max_value=6,
        value=3
    )

    grade = st.selectbox(
        "Grade",
        list(grades.keys())
    )

    if st.button("➕ Add Course"):

        quality_point = credit * grades[grade]

        st.session_state.courses.append({

            "Course Code": code.upper(),

            "Course Title": title,

            "Credit Unit": credit,

            "Grade": grade,

            "Quality Point": quality_point

        })

        st.success("Course added successfully.")

    # ==========================
    # DISPLAY COURSES
    # ==========================

    if len(st.session_state.courses) > 0:

        st.divider()

        df = pd.DataFrame(st.session_state.courses)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        total_units = df["Credit Unit"].sum()

        total_quality = df["Quality Point"].sum()

        gpa = total_quality / total_units

        st.metric(
            "Semester GPA",
            f"{gpa:.2f}"
        )

        st.divider()

        previous_cgpa = st.number_input(
            "Previous CGPA",
            min_value=0.00,
            max_value=5.00,
            value=0.00,
            step=0.01
        )

        # Simple CGPA estimate
        if previous_cgpa == 0:
            cgpa = gpa
        else:
            cgpa = (previous_cgpa + gpa) / 2

        st.metric(
            "Current CGPA",
            f"{cgpa:.2f}"
        )

        if st.button(
            "💾 Save Result",
            use_container_width=True
        ):

            database.save_result(
                st.session_state.username,
                session,
                semester,
                round(gpa, 2),
                round(cgpa, 2)
            )

            st.success("Result saved successfully.")

            st.session_state.courses = []

            st.rerun()
