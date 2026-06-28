import streamlit as st
import pandas as pd
import database


def show():

    st.title("👤 My Profile")

    # ======================================
    # USER INFORMATION
    # ======================================

    user = database.get_user(
        st.session_state.username
    )

    if user:

        st.subheader("Account Information")

        st.write(f"**Username:** {user[1]}")
        st.write(f"**Email:** {user[2]}")

    st.divider()

    # ======================================
    # STATISTICS
    # ======================================

    stats = database.get_statistics(
        st.session_state.username
    )

    total_saved = stats[0] if stats[0] else 0
    highest = stats[1] if stats[1] else 0.00
    average = stats[2] if stats[2] else 0.00

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Saved Results",
        total_saved
    )

    c2.metric(
        "Highest CGPA",
        f"{highest:.2f}"
    )

    c3.metric(
        "Average CGPA",
        f"{average:.2f}"
    )

    st.divider()

    # ======================================
    # RECENT CALCULATIONS
    # ======================================

    history = database.get_history(
        st.session_state.username
    )

    if history:

        df = pd.DataFrame(

            history,

            columns=[
                "ID",
                "Session",
                "Semester",
                "Semester GPA",
                "CGPA",
                "Credit Units",
                "Quality Points",
                "Classification",
                "Date"
            ]

        )

        st.subheader("Recent Calculations")

        st.dataframe(

            df.drop(columns=["ID"]).head(5),

            use_container_width=True,

            hide_index=True

        )

        st.divider()

        st.subheader("CGPA Progress")

        chart = df.iloc[::-1][["CGPA"]]

        st.line_chart(chart)

    else:

        st.info(
            "No saved calculations yet."
        )

    st.divider()

    # ======================================
    # QUICK SUMMARY
    # ======================================

    if history:

        latest = df.iloc[0]

        st.subheader("Latest Result")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Latest GPA",
                f"{latest['Semester GPA']:.2f}"
            )

        with col2:
            st.metric(
                "Latest CGPA",
                f"{latest['CGPA']:.2f}"
            )

        st.success(
            f"Current Standing: {latest['Classification']}"
        )

    st.divider()

    # ======================================
    # LOGOUT
    # ======================================

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):

        st.session_state.logged_in = False
        st.session_state.username = ""

        st.rerun()
