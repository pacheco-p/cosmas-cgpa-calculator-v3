import streamlit as st
import pandas as pd
import database


def show():

    st.title("⚙️ Admin Panel")

    st.caption("Manage course lists for different departments.")

    st.divider()

    # ==================================
    # ADD COURSE
    # ==================================

    st.subheader("➕ Add Course")

    with st.form("add_course"):

        department = st.text_input(
            "Department"
        )

        level = st.selectbox(
            "Level",
            [
                "100 Level",
                "200 Level",
                "300 Level",
                "400 Level",
                "500 Level",
                "600 Level"
            ]
        )

        semester = st.selectbox(
            "Semester",
            [
                "First Semester",
                "Second Semester"
            ]
        )

        course_code = st.text_input(
            "Course Code"
        )

        credit_unit = st.number_input(
            "Credit Unit",
            min_value=1,
            max_value=10,
            value=3
        )

        submit = st.form_submit_button(
            "Add Course",
            use_container_width=True
        )

        if submit:

            if department.strip() == "" or course_code.strip() == "":

                st.error(
                    "Department and Course Code are required."
                )

            else:

                database.add_course(
                    department.strip(),
                    level,
                    semester,
                    course_code.strip().upper(),
                    credit_unit
                )

                st.success(
                    "Course added successfully."
                )

                st.rerun()

    st.divider()

    # ==================================
    # VIEW COURSES
    # ==================================

    st.subheader("📚 View Courses")

    search_department = st.text_input(
        "Department",
        key="search_department"
    )

    search_level = st.selectbox(
        "Level",
        [
            "100 Level",
            "200 Level",
            "300 Level",
            "400 Level",
            "500 Level",
            "600 Level"
        ],
        key="search_level"
    )

    search_semester = st.selectbox(
        "Semester",
        [
            "First Semester",
            "Second Semester"
        ],
        key="search_semester"
    )

    if st.button("Load Courses"):

        courses = database.get_courses(
            search_department.strip(),
            search_level,
            search_semester
        )

        if len(courses) == 0:

            st.warning(
                "No courses found."
            )

        else:

            df = pd.DataFrame(courses)

            st.dataframe(
                df[
                    [
                        "id",
                        "course_code",
                        "credit_unit"
                    ]
                ],
                use_container_width=True
            )

            course_ids = df["id"].tolist()

            delete_id = st.selectbox(
                "Select Course ID to Delete",
                course_ids
            )

            if st.button("🗑 Delete Course"):

                database.delete_course(delete_id)

                st.success(
                    "Course deleted."
                )

                st.rerun()
