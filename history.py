import streamlit as st
import pandas as pd

def show(get_history_func, delete_history_func):
    st.title("Historical Record Timelines")
    history_data = get_history_func(st.session_state.username)
    
    if history_data:
        df = pd.DataFrame(
            history_data, 
            columns=["Record ID", "GPA", "CGPA", "Total Units", "Quality Points", "Academic Term Log", "Timestamp Saved"]
        )
        
        st.subheader("Logged Calculations Matrix Table")
        st.dataframe(df.drop(columns=["Record ID"]), use_container_width=True, hide_index=True)
        
        st.divider()
        st.subheader("Manage System Ledger Cleanups")
        with st.expander("Remove Academic Standings Entry"):
            options_map = {f"{r[5]} (Logged {r[6]})": r[0] for r in history_data}
            selected_key = st.selectbox("Select calculation matrix line to purge:", list(options_map.keys()))
            
            if st.button("Purge Entry Data Block", type="primary"):
                delete_history_func(options_map[selected_key])
                st.success("Target records removed from dashboard processing logs.")
                st.rerun()
    else:
        st.info("No timeline metrics logged on this profile yet.")
