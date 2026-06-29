import streamlit as st
import pandas as pd
import database


def show():

    st.title("🏠 Dashboard")

    st.write(f"### Welcome, {st.session_state.username} 👋")

    user = database.get_user(st.session_state.username)

    if user:

        col1, col2 = st.columns(2)

        with col1:
            st.info(f"**Full Name:** {user['full_name'] or 'Not Set'}")
            st.info(f"**Matric No:** {user['matric_number'] or 'Not Set'}")
            st.info(f"**Department:** {user['department'] or 'Not Set'}")

        with col2:
            st.info(f"**Faculty:** {user['faculty'] or 'Not Set'}")
            st.info(f"**Level:** {user['level'] or 'Not Set'}")
            st.info(f"**Admission Year:** {user['admission_year'] or 'Not Set'}")

    st.divider()

    results = database.get_results(st.session_state.username)

    if not results:

        st.warning("No CGPA records found.")

        return

    df = pd.DataFrame(results)

    latest = df.iloc[0]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Latest GPA",
            f"{latest['gpa']:.2f}"
        )

    with col2:
        st.metric(
            "Latest CGPA",
            f"{latest['cgpa']:.2f}"
        )

    with col3:
        st.metric(
            "Saved Results",
            len(df)
        )

    st.divider()

    st.subheader("Recent Results")

    st.dataframe(
        df[
            [
                "session",
                "semester",
                "gpa",
                "cgpa",
                "created_at"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.subheader("CGPA Progress")

    chart = df.iloc[::-1].set_index("created_at")["cgpa"]

    st.line_chart(chart)
