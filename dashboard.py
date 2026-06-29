import streamlit as st
import pandas as pd
import database

def show():
    try:
        st.image("assets/cosmas_banner.png", use_container_width=True)
    except:
        st.title("🏛️ COSMAS AT SUG TOP SEAT")

    st.title("🏠 Dashboard")
    st.success(f"Welcome back, {st.session_state.username}! 👋")

    # -----------------------------
    # Statistics Calculation
    # -----------------------------
    stats = database.get_statistics(st.session_state.username)
    total_saved = stats[0] if stats[0] else 0
    highest = stats[1] if stats[1] else 0.00
    average = stats[2] if stats[2] else 0.00

    history_data = database.get_history(st.session_state.username)
    latest = history_data[0][2] if history_data else 0.00

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Saved Semesters", total_saved)
    c2.metric("Latest CGPA", f"{latest:.2f}")
    c3.metric("Highest CGPA", f"{highest:.2f}")
    c4.metric("Average CGPA", f"{average:.2f}")

    st.divider()

    # -----------------------------
    # Recent Activity Table
    # -----------------------------
    st.subheader("📋 Recent Calculations")
    if history_data:
        recent = pd.DataFrame(
            history_data,
            columns=["ID", "GPA", "CGPA", "Credit Units", "Quality Points", "Semester", "Date"]
        )
        st.dataframe(
            recent[["Semester", "GPA", "CGPA", "Credit Units", "Date"]],
            use_container_width=True,
            hide_index=True
        )

        st.divider()
        st.subheader("📈 CGPA Progress Trend")
        chart_df = recent.iloc[::-1].copy()
        chart_df = chart_df.set_index("Semester")[["CGPA"]]
        st.line_chart(chart_df)
    else:
        st.info("No saved calculations yet. Add records in the calculator tab.")

    st.divider()

    # Motivation Blocks
    st.subheader("🎯 Academic Goal Status")
    if latest >= 4.50:
        st.success("Excellent work! You're maintaining a First Class. Keep it up! 🏆")
    elif latest >= 3.50:
        st.info("You're in Second Class Upper. A little extra effort can get you to First Class.")
    elif latest >= 2.40:
        st.warning("You're in Second Class Lower. Stay focused—you can still improve your CGPA.")
    elif latest >= 1.50:
        st.warning("You're currently in Third Class. Every semester is a chance to climb higher.")
    else:
        st.error("Your CGPA needs attention. Stay determined and improve one course at a time.")
