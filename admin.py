import streamlit as st
import pandas as pd
import database

ADMIN_USERS = ["admin", "cosmas", "pedro"]

def show():

    st.title("⚙️ Admin Panel")

    if st.session_state.username.lower() not in ADMIN_USERS:
        st.error("Access denied. Admins only.")
        return

    st.success("Administrator Access Granted")

    st.subheader("Add Course")

    with st.form("course_form"):

        department = st.text_input("Department")

        level = st.selectbox(
            "Level",
            ["100 Level","200 Level","300 Level","400 Level","500 Level","600 Level"]
        )

        semester = st.selectbox(
            "Semester",
            ["First Semester","Second Semester"]
        )

        course_code = st.text_input("Course Code")

        credit_unit = st.number_input(
            "Credit Unit",
            min_value=1,
            max_value=10,
            value=3
        )

        if st.form_submit_button("Add Course"):

            database.add_course(
                department,
                level,
                semester,
                course_code.upper(),
                credit_unit
            )

            st.success("Course added successfully.")

    st.divider()

    st.subheader("Course List")

    dept = st.text_input("Search Department")

    if st.button("Load Courses"):

        courses = database.get_all_courses(dept)

        if courses:

            df = pd.DataFrame(courses)

            st.dataframe(df, use_container_width=True)

        else:

            st.info("No courses found.")
