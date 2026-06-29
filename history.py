import streamlit as st
import pandas as pd

def show(get_history_func, delete_history_func):
    st.title("Calculation History")
    
    history_data = get_history_func(st.session_state.username)
    
    if history_data:
        df = pd.DataFrame(
            history_data, 
            columns=["Record ID", "GPA", "CGPA", "Total Units", "Quality Points", "Academic Term", "Date Saved"]
        )
        
        st.subheader("Saved Academic Standings")
        st.dataframe(
            df.drop(columns=["Record ID"]), 
            use_container_width=True,
            hide_index=True
        )
        
        st.divider()
        
        st.subheader("Manage Logs")
        with st.expander("Delete an Academic Record"):
            record_options = {
                f"{row[5]} (Saved on {row[6]})": row[0] for row in history_data
            }
            
            selected_label = st.selectbox("Select record to clear:", list(record_options.keys()))
            
            if st.button("Delete Permanently", type="primary"):
                record_id_to_delete = record_options[selected_label]
                delete_history_func(record_id_to_delete)
                st.success("Record cleared successfully.")
                st.rerun()
    else:
        st.info("Your calculation logs are completely empty. Save a profile from the CGPA Calculator tab to build your timeline.")
