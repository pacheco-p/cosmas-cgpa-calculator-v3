import streamlit as st
import pandas as pd
import database


def show():

    st.title("📊 Result History")

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

    st.subheader("Saved Results")

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

    # ==========================
    # SEARCH
    # ==========================

    search = st.text_input(
        "🔍 Search Session"
    )

    if search:

        filtered = df[
            df["Session"].str.contains(
                search,
                case=False
            )
        ]

        st.dataframe(

            filtered[
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

    # ==========================
    # DELETE RESULT
    # ==========================

    record = st.selectbox(

        "Select Result",

        df["ID"]

    )

    if st.button(
        "🗑 Delete Result",
        use_container_width=True
    ):

        database.delete_result(
            int(record)
        )

        st.success(
            "Result deleted successfully."
        )

        st.rerun()

    st.divider()

    # ==========================
    # CGPA CHART
    # ==========================
