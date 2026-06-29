import streamlit as st
import pandas as pd
import io
import database

def show():
    st.title("📊 Calculation History")

    history_data = database.get_history(st.session_state.username)

    if not history_data:
        st.info("You haven't saved any calculations yet.")
        return

    df = pd.DataFrame(
        history_data,
        columns=["ID", "Semester GPA", "CGPA", "Credit Units", "Quality Points", "Semester", "Date"]
    )

    # Summary Row
    c1, c2, c3 = st.columns(3)
    c1.metric("Saved Entries", len(df))
    c2.metric("Highest CGPA", f"{df['CGPA'].max():.2f}")
    c3.metric("Average CGPA", f"{df['CGPA'].mean():.2f}")

    st.divider()

    search = st.text_input("🔍 Filter by Level / Semester Name")
    if search:
        df = df[df["Semester"].astype(str).str.contains(search, case=False)]

    st.subheader("Saved Calculations Log")
    st.dataframe(
        df[["Semester", "Semester GPA", "CGPA", "Credit Units", "Quality Points", "Date"]],
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.subheader("Delete a Record")
    record_map = dict(zip(df["Semester"] + " (" + df["Date"] + ")", df["ID"]))
    record_select = st.selectbox("Select Record to Erase:", list(record_map.keys()))

    if st.button("🗑 Delete Record", use_container_width=True):
        database.delete_history(int(record_map[record_select]))
        st.success("Record deleted successfully.")
        st.rerun()
