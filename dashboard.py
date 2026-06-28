# dashboard.py
import streamlit as st
import pandas as pd
import database

def show():
    st.title("🏠 Dashboard")
    st.success(f"Welcome back, {st.session_state.username}! 👋")

    stats = database.get_statistics(st.session_state.username)
    total_saved = stats[0] or 0
    highest = stats[1] or 0.0
    average = stats[2] or 0.0

    history = database.get_history(st.session_state.username)

    latest = history[0][4] if history else 0.0

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Saved Results", total_saved)
    c2.metric("Latest CGPA", f"{latest:.2f}")
    c3.metric("Highest CGPA", f"{highest:.2f}")
    c4.metric("Average CGPA", f"{average:.2f}")

    st.divider()

    if history:
        df = pd.DataFrame(history, columns=[
            "ID","Session","Semester","Semester GPA","CGPA",
            "Credit Units","Quality Points","Classification","Date"
        ])

        st.subheader("Recent Calculations")
        st.dataframe(
            df.drop(columns=["ID"]).head(5),
            use_container_width=True,
            hide_index=True
        )

        st.subheader("📈 CGPA Progress")
        st.line_chart(df.iloc[::-1][["CGPA"]])

        st.subheader("🏅 Current Classification")
        st.info(df.iloc[0]["Classification"])

    else:
        st.info("No saved calculations yet.")