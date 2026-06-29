import streamlit as st
import pandas as pd
import database

def show():
    st.title("📜 Result History")
    rows=database.get_results(st.session_state.username)
    if not rows:
        st.info("No saved results yet.")
        return
    df=pd.DataFrame(rows)
    st.dataframe(df,use_container_width=True)
