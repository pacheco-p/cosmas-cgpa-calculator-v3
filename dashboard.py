import streamlit as st
import database

def show():
    st.title("🏠 Dashboard")

    user = database.get_user(st.session_state.username)

    if not user:
        st.error("User not found.")
        return

    st.subheader(f"Welcome, {user['full_name'] or user['username']} 👋")

    c1, c2 = st.columns(2)
    c1.metric("Department", user["department"] or "-")
    c2.metric("Current Level", user["current_level"] or "-")

    results = database.get_results(st.session_state.username)

    if results:
        latest = results[0]

        st.divider()

        a, b, c = st.columns(3)

        a.metric("Current CGPA", f"{latest['cgpa']:.2f}")
        b.metric("Latest GPA", f"{latest['gpa']:.2f}")
        c.metric("Semesters Saved", len(results))

        cgpa = latest["cgpa"]

        if cgpa >= 4.50:
            st.success("🏆 First Class")
        elif cgpa >= 3.50:
            st.info("🥇 Second Class Upper")
        elif cgpa >= 2.40:
            st.info("🥈 Second Class Lower")
        elif cgpa >= 1.50:
            st.warning("🎓 Third Class")
        else:
            st.error("⚠️ Pass")

    else:
        st.info("No calculation history yet.")
