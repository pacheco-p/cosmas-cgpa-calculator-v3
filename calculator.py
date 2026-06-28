import streamlit as st
import pandas as pd
import database


def show():

    st.title("🎓 CGPA Calculator")

    # ==========================
    # STUDENT PROFILE
    # ==========================

    user = database.get_user(st.session_state.username)

    if not user:
        st.error("User not found.")
        return

    st.subheader("Student Information")

    col1, col2 = st.columns(2)

    with col1:
        st.write(f"**Name:** {user['full_name'] or 'Not Set'}")
        st.write(f"**Matric No:** {user['matric_number'] or 'Not Set'}")
        st.write(f"**Department:** {user['department'] or 'Not Set'}")

    with col2:
        st.write(f"**Faculty:** {user['faculty'] or 'Not Set'}")
        st.write(f"**Level:** {user['level'] or 'Not Set'}")

    st.divider()

    session = st.text_input("Academic Session", "2025/2026")

    semester = st.selectbox(
        "Semester",
        [
            "First Semester",
            "Second Semester"
        ]
    )

    st.divider()

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

    cu = st.number_input(
        "Credit Unit",
        1,
        6,
        3
    )

    grade = st.selectbox(
        "Grade",
        list(grades.keys())
    )

    if st.button("➕ Add Course"):

        qp = cu * grades[grade]

        st.session_state.courses.append({

            "Course Code": code.upper(),

            "Course Title": title,

            "Credit Unit": cu,

            "Grade": grade,

            "Quality Point": qp

        })

        st.success("Course added successfully.")

    if st.session_state.courses:

        st.divider()

        df = pd.DataFrame(st.session_state.courses)

        st.dataframe(
            df,
            use_container_width=True
        )

        total_cu = df["Credit Unit"].sum()

        total_qp = df["Quality Point"].sum()

        gpa = total_qp / total_cu

        st.metric(
            "Semester GPA",
            f"{gpa:.2f}"
        )

        previous_cgpa = st.number_input(
            "Previous CGPA",
            0.00,
            5.00,
            0.00
        )

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

                gpa,

                cgpa

            )

            st.success(
                "Result saved successfully."
            )
            # ==========================
# GPA
# ==========================

total_cu = df["Credit Unit"].sum()
total_qp = df["Quality Point"].sum()

gpa = total_qp / total_cu

st.metric("Semester GPA", f"{gpa:.2f}")

st.divider()

st.subheader("Previous Academic Record")

previous_units = st.number_input(
    "Previous Total Credit Units",
    min_value=0,
    value=0
)

previous_qp = st.number_input(
    "Previous Quality Points",
    min_value=0.0,
    value=0.0,
    step=0.01
)

current_qp = total_qp
current_units = total_cu

overall_qp = previous_qp + current_qp
overall_units = previous_units + current_units

if overall_units > 0:
    cgpa = overall_qp / overall_units
else:
    cgpa = gpa

st.metric("Current CGPA", f"{cgpa:.2f}")

col1, col2 = st.columns(2)

with col1:
    st.metric("Current Credit Units", current_units)

with col2:
    st.metric("Total Credit Units", overall_units)

if st.button("💾 Save Result", use_container_width=True):

    database.save_result(
        st.session_state.username,
        session,
        semester,
        round(gpa, 2),
        round(cgpa, 2)
    )

    st.success("Result saved successfully.")

    st.session_state.courses = []
