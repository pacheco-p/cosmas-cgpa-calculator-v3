import streamlit as st
import pandas as pd
import database


def show():

    st.title("🛠 Admin Panel")

    st.info("Add courses for each Department, Level and Semester.")

    department = st.text_input("Department")

    level = st.selectbox(
        "Level",
        [
            "100 Level",
            "200 Level",
            "300 Level",
            "400 Level",
            "500 Level"
        ]
    )

    semester = st.selectbox(
        "Semester",
        [
            "First Semester",
            "Second Semester"
        ]
    )

    st.divider()

    course_code = st.text_input("Course Code")

    course_title = st.text_input("Course Title")

    credit_unit = st.number_input(
        "Credit Unit",
        min_value=1,
        max_value=6,
        value=3
    )

    if st.button(
        "➕ Add Course",
        use_container_width=True
    ):

        database.add_course(
            department,
            level,
            semester,
            course_code.upper(),
            course_title,
            credit_unit
        )

        st.success("Course added successfully.")

    st.divider()

    st.subheader("Registered Courses")

    if department:

        courses = database.get_courses(
            department,
            level,
            semester
        )

        if courses:

            df = pd.DataFrame(
                courses,
                columns=[
                    "ID",
                    "Department",
                    "Level",
                    "Semester",
                    "Course Code",
                    "Course Title",
                    "Credit Unit"
                ]
            )

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

            course_id = st.selectbox(
                "Select Course",
                df["ID"]
            )

            if st.button(
                "🗑 Delete Course",
                use_container_width=True
            ):

                database.delete_course(
                    int(course_id)
                )

                st.success("Course deleted.")

                st.rerun()

        else:

            st.warning(
                "No course added yet."
            )