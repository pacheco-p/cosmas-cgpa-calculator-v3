import streamlit as st
import pandas as pd
import database

def show():
    st.title("👤 My Profile")
    st.subheader("Account Information")

    user = database.get_user(st.session_state.username)
    if user:
        st.write(f"**Username:** {user[1]}")
        st.write(f"**Email:** {user[2]}")

    st.divider()

    stats = database.get_statistics(st.session_state.username)
    total_saved = stats[0] if stats[0] else 0
    highest = stats[1] if stats[1] else 0.00
    average = stats[2] if stats[2] else 0.00

    col1, col2, col3 = st.columns(3)
    col1.metric("Saved Semesters", total_saved)
    col2.metric("Highest CGPA", f"{highest:.2f}")
    col3.metric("Average CGPA", f"{average:.2f}")

    st.divider()

    st.subheader("📋 Academic Summary Summary")
    history_data = database.get_history(st.session_state.username)

    if history_data:
        df = pd.DataFrame(
            history_data,
            columns=["ID", "Semester GPA", "CGPA", "Credit Units", "Quality Points", "Semester", "Date"]
        )
        st.dataframe(
            df[["Semester", "Semester GPA", "CGPA", "Date"]],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No calculations stored yet.")
