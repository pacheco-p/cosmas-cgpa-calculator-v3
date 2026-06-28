import streamlit as st
import pandas as pd
import io
import database

# ==========================
# GRADE POINTS
# ==========================

GRADES = {
    "A": 5,
    "B": 4,
    "C": 3,
    "D": 2,
    "E": 1,
    "F": 0
}


# ==========================
# DEGREE CLASSIFICATION
# ==========================

def get_classification(cgpa):

    if cgpa >= 4.50:
        return "🏆 First Class"

    elif cgpa >= 3.50:
        return "🥇 Second Class Upper"

    elif cgpa >= 2.40:
        return "🥈 Second Class Lower"

    elif cgpa >= 1.50:
        return "🎓 Third Class"

    else:
        return "⚠️ Pass"


# ==========================
# MAIN PAGE
# ==========================

def show():

    st.title("🎓 CGPA Calculator")

    # --------------------------
    # Session State
    # --------------------------

    if "courses" not in st.session_state:
        st.session_state.courses = []

    # --------------------------
    # Academic Information
    # --------------------------

    st.subheader("Academic Information")

    col1, col2 = st.columns(2)

    with col1:

        session = st.text_input(
            "Academic Session",
            value="2025/2026"
        )

    with col2:

        semester = st.selectbox(
            "Semester",
            [
                "First Semester",
                "Second Semester"
            ]
        )

    st.divider()

    # --------------------------
    # Previous Record
    # --------------------------

    st.subheader("Previous Academic Record")

    col1, col2 = st.columns(2)

    with col1:

        previous_cu = st.number_input(
            "Previous Credit Units",
            min_value=0,
            value=0
        )

    with col2:

        previous_qp = st.number_input(
            "Previous Quality Points",
            min_value=0.0,
            value=0.0
        )

    st.divider()

    # --------------------------
    # Add Course
    # --------------------------

    st.subheader("Add Course")

    with st.form("course_form"):

        course_code = st.text_input(
            "Course Code"
        )

        col1, col2 = st.columns(2)

        with col1:

            credit_unit = st.number_input(
                "Credit Unit",
                min_value=1,
                max_value=6,
                value=3
            )

        with col2:

            grade = st.selectbox(
                "Grade",
                list(GRADES.keys())
            )

        add_course = st.form_submit_button(
            "➕ Add Course"
        )

        if add_course:

            course_code = course_code.strip().upper()

            if course_code == "":

                st.error("Course code cannot be empty.")

            elif any(
                c["Course"] == course_code
                for c in st.session_state.courses
            ):

                st.warning("Course already exists.")

            else:

                st.session_state.courses.append({

                    "Course": course_code,

                    "Credit Units": credit_unit,

                    "Grade": grade,

                    "GP": GRADES[grade],

                    "Quality Points":
                        credit_unit * GRADES[grade]

                })

                st.success(
                    f"{course_code} added successfully."
                )

                st.rerun()
                # --------------------------
    # Display Courses
    # --------------------------

    if st.session_state.courses:

        df = pd.DataFrame(st.session_state.courses)

        semester_cu = df["Credit Units"].sum()
        semester_qp = df["Quality Points"].sum()

        semester_gpa = semester_qp / semester_cu

        total_cu = previous_cu + semester_cu
        total_qp = previous_qp + semester_qp

        cgpa = total_qp / total_cu

        classification = get_classification(cgpa)

        st.divider()

        st.subheader("Result")

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Semester GPA",
            f"{semester_gpa:.2f}"
        )

        c2.metric(
            "Current CGPA",
            f"{cgpa:.2f}"
        )

        c3.metric(
            "Classification",
            classification
        )

        st.divider()

        st.subheader("Registered Courses")

        st.dataframe(
            df[
                [
                    "Course",
                    "Credit Units",
                    "Grade",
                    "Quality Points"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        delete_course = st.selectbox(
            "Select Course to Delete",
            df["Course"]
        )

        if st.button(
            "🗑 Delete Course",
            use_container_width=True
        ):

            st.session_state.courses = [

                course

                for course in st.session_state.courses

                if course["Course"] != delete_course

            ]

            st.success("Course deleted successfully.")

            st.rerun()

        st.divider()

        if st.button(
            "💾 Save Calculation",
            use_container_width=True
        ):

            history_id = database.save_history(

                st.session_state.username,

                session,

                semester,

                semester_gpa,

                cgpa,

                total_cu,

                total_qp,

                classification

            )

            database.save_courses(

                history_id,

                st.session_state.courses

            )

            st.success(
                "Calculation saved successfully."
            )

        st.divider()

        csv = io.BytesIO()

        df.to_csv(
            csv,
            index=False
        )

        st.download_button(

            "📥 Download Result (CSV)",

            csv.getvalue(),

            file_name="cgpa_result.csv",

            mime="text/csv",

            use_container_width=True

        )

    else:

        st.info(
            "No course has been added yet."
        )
                
