# history.py
import streamlit as st
import pandas as pd
import io
import database

def show():
    st.title("📊 Calculation History")
    history=database.get_history(st.session_state.username)
    if not history:
        st.info("No saved calculations.")
        return
    df=pd.DataFrame(history,columns=[
        "ID","Session","Semester","Semester GPA","CGPA",
        "Credit Units","Quality Points","Classification","Date"
    ])
    st.dataframe(df,use_container_width=True,hide_index=True)

    st.subheader("View Courses")
    rid=st.selectbox("Select Record",df["ID"])
    if st.button("Show Courses"):
        c=database.get_courses(int(rid))
        if c:
            cdf=pd.DataFrame(c,columns=[
                "Course","Credit Units","Grade","Grade Point","Quality Points"
            ])
            st.dataframe(cdf,use_container_width=True,hide_index=True)
        else:
            st.info("No courses found.")

    if st.button("🗑 Delete Selected Record"):
        database.delete_history(int(rid))
        st.success("Deleted.")
        st.rerun()

    buf=io.BytesIO()
    df.to_csv(buf,index=False)
    st.download_button("📥 Download CSV",buf.getvalue(),"history.csv","text/csv")