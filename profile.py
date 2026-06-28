# profile.py
import streamlit as st
import pandas as pd
import database

def show():
    st.title("👤 My Profile")
    user=database.get_user(st.session_state.username)
    if user:
        st.write(f"**Username:** {user[1]}")
        st.write(f"**Email:** {user[2]}")
    st.divider()

    stats=database.get_statistics(st.session_state.username)
    c1,c2,c3=st.columns(3)
    c1.metric("Saved Results",stats[0] or 0)
    c2.metric("Highest CGPA",f"{(stats[1] or 0):.2f}")
    c3.metric("Average CGPA",f"{(stats[2] or 0):.2f}")

    hist=database.get_history(st.session_state.username)
    if hist:
        df=pd.DataFrame(hist,columns=[
            "ID","Session","Semester","Semester GPA","CGPA",
            "Credit Units","Quality Points","Classification","Date"
        ])
        st.subheader("Recent Results")
        st.dataframe(df.drop(columns=["ID"]).head(5),hide_index=True,use_container_width=True)
        st.subheader("CGPA Progress")
        st.line_chart(df.iloc[::-1][["CGPA"]])
    else:
        st.info("No saved calculations.")