import streamlit as st
import pandas as pd
import database


def show():

    st.title("🏠 Dashboard")

    st.success(
        f"Welcome, {st.session_state.username} 👋"
    )

    results = database.get_results(
        st.session_state.username
    )

    if not results:

        st.info(
            "No saved results yet."
        )

        return

    df = pd.DataFrame(

        results,

        columns=[
            "ID",
            "Username",
            "Session",
            "Semester",
            "GPA",
            "CGPA",
            "Date"
        ]

    )

    latest = df.iloc[0]

    total_results = len(df)

    highest = df["CGPA"].max()

    average = df["CGPA"].mean()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Saved Results",
        total_results
    )

    col2.metric(
        "Latest CGPA",
        f"{latest['CGPA']:.2f}"
    )

    col3.metric(
        "Highest CGPA",
        f"{highest:.2f}"
    )

    col4.metric(
        "Average CGPA",
        f"{average:.2f}"
    )

    st.divider()

    st.subheader("Latest Results")

    st.dataframe(

        df[
            [
                "Session",
                "Semester",
                "GPA",
                "CGPA",
                "Date"
            ]
        ],

        use_container_width=True,

        hide_index=True

    )

    st.divider()

    st.subheader("📈 CGPA Progress")

    chart = df.iloc[::-1][["CGPA"]]

    st.line_chart(chart)

    st.divider()

    latest_cgpa = latest["CGPA"]

    st.subheader("Academic Standing")

    if latest_cgpa >= 4.50:

        st.success("🏆 First Class")

    elif latest_cgpa >= 3.50:

        st.info("🥇 Second Class Upper")

    elif latest_cgpa >= 2.40:

        st.warning("🥈 Second Class Lower")

    elif latest_cgpa >= 1.50:

        st.warning("🎓 Third Class")

    else:

        st.error("⚠️ Pass")
