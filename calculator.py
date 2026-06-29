import streamlit as st
import database

GRADES={"A":5,"B":4,"C":3,"D":2,"E":1,"F":0}

def show():
    st.title("🎓 CGPA Calculator")
    user=database.get_user(st.session_state.username)
    if not user:
        st.error("Complete your profile.")
        return
    session=st.text_input("Academic Session","2025/2026")
    level=st.selectbox("Level",["100 Level","200 Level","300 Level","400 Level","500 Level","600 Level"])
    semester=st.selectbox("Semester",["First Semester","Second Semester"])
    courses=database.get_courses(user["department"],level,semester)
    if not courses:
        st.warning("No courses found.")
        return
    total_cu=0
    total_qp=0
    for c in courses:
        g=st.selectbox(f'{c["course_code"]} ({c["credit_unit"]} CU)',list(GRADES.keys()),key=str(c["id"]))
        total_cu+=c["credit_unit"]
        total_qp+=c["credit_unit"]*GRADES[g]
    if st.button("Calculate"):
        gpa=total_qp/total_cu if total_cu else 0
        prev=database.get_previous_result(st.session_state.username)
        if prev:
            grand_cu=prev["total_credit_units"]+total_cu
            grand_qp=prev["total_quality_points"]+total_qp
        else:
            grand_cu,total_cu
            grand_cu=total_cu
            grand_qp=total_qp
        cgpa=grand_qp/grand_cu if grand_cu else 0
        st.metric("GPA",f"{gpa:.2f}")
        st.metric("CGPA",f"{cgpa:.2f}")
        if st.button("Save Result"):
            database.save_result(st.session_state.username,session,level,semester,gpa,cgpa,grand_cu,grand_qp)
            st.success("Saved.")
