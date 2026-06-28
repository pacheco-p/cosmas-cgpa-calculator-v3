import streamlit as st
import pandas as pd
import database


def show():

    st.title("🏠 Dashboard")

    st.success(
        f"Welcome back, {st.session_state.username}! 👋"
    )

    # =====================================
    # Statistics
    # =====================================

    stats = database.get_statistics(
        st.session_state.username
    )

    total_saved = stats[0] if stats[0] else 0
    highest = stats[1] if stats[1] else 0.00
    average = stats[2] if stats[2] else 0.00

    history = database.get_history(
        st.session_state.username
    )

    latest = history[0][4] if history else 0.00

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Saved Results",
        total_saved
    )

    c2.metric(
        "Latest CGPA",
        f"{latest:.2f}"
    )

    c3.metric(
        "Highest CGPA",
        f"{highest:.2f}"
    )

    c4.metric(
        "Average CGPA",
        f"{average:.2f}"
    )

    st.divider()

    # =====================================
    # Recent Calculations
    # =====================================

    st.subheader("📋 Recent Calculations")

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

        st.dataframe(

            df.drop(columns=["ID"]),

            use_container_width=True,

            hide_index=True

        )

        st.divider()

        # =====================================
        # CGPA Progress
        # =====================================

        st.subheader("📈 CGPA Progress")

        chart = df.iloc[::-1][["CGPA"]]

        st.line_chart(chart)

        st.divider()

        # =====================================
        # Current Standing
        # =====================================

        latest_class = df.iloc[0]["Classification"]

        st.subheader("🎯 Current Academic Standing")

        if "First Class" in latest_class:

            st.success(
                latest_class
            )

        elif "Second Class Upper" in latest_class:

            st.info(
                latest_class
            )

        elif "Second Class Lower" in latest_class:

            st.warning(
                latest_class
            )

        else:

            st.error(
                latest_class
            )

    else:

        st.info(
            "No saved calculations yet."
        )
