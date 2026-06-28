# calculator.py
import streamlit as st
import pandas as pd
import io
import database

GRADES={"A":5,"B":4,"C":3,"D":2,"E":1,"F":0}

def classify(cgpa):
    if cgpa>=4.50: return "🏆 First Class"
    if cgpa>=3.50: return "🥇 Second Class Upper"
    if cgpa>=2.40: return "🥈 Second Class Lower"
    if cgpa>=1.50: return "🎓 Third Class"
    return "⚠️ Pass"

def show():
    st.title("🎓 CGPA Calculator")

    if "courses" not in st.session_state:
        st.session_state.courses=[]

    session=st.text_input("Academic Session","2025/2026")
    semester=st.selectbox("Semester",["First Semester","Second Semester"])

    c1,c2=st.columns(2)
    with c1:
        prev_cu=st.number_input("Previous Credit Units",0,value=0)
    with c2:
        prev_qp=st.number_input("Previous Quality Points",0.0,value=0.0)

    with st.form("course"):
        code=st.text_input("Course Code")
        a,b=st.columns(2)
        with a:
            cu=st.number_input("Credit Units",1,6,3)
        with b:
            grade=st.selectbox("Grade",list(GRADES))
        if st.form_submit_button("Add Course"):
            code=code.strip().upper()
            if code:
                st.session_state.courses.append({
                    "Course":code,
                    "Credit Units":cu,
                    "Grade":grade,
                    "GP":GRADES[grade],
                    "Quality Points":cu*GRADES[grade]
                })
                st.rerun()

    if not st.session_state.courses:
        st.info("Add at least one course.")
        return

    df=pd.DataFrame(st.session_state.courses)
    total_cu=df["Credit Units"].sum()
    total_qp=df["Quality Points"].sum()
    gpa=total_qp/total_cu
    grand_cu=prev_cu+total_cu
    grand_qp=prev_qp+total_qp
    cgpa=grand_qp/grand_cu if grand_cu else 0
    cls=classify(cgpa)

    x,y,z,w=st.columns(4)
    x.metric("Semester GPA",f"{gpa:.2f}")
    y.metric("CGPA",f"{cgpa:.2f}")
    z.metric("Credit Units",grand_cu)
    w.metric("Classification",cls)

    st.dataframe(df,use_container_width=True)

    if st.button("💾 Save Result"):
        hid=database.save_history(
            st.session_state.username,session,semester,
            gpa,cgpa,grand_cu,grand_qp,cls
        )
        database.save_courses(hid,st.session_state.courses)
        st.success("Saved successfully.")

    csv=io.BytesIO()
    df.to_csv(csv,index=False)
    st.download_button("Download CSV",csv.getvalue(),"cgpa.csv","text/csv")