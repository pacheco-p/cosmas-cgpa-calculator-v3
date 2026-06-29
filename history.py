import streamlit as st
import pandas as pd

def show(get_history_func, delete_history_func):
    st.title("Calculation History")
    
    # Retrieve all logged calculations
    history_data = get_history_func(st.session_state.username)
    
    if history_data:
        # Map raw SQLite tuples into a structured DataFrame
        df = pd.DataFrame(
            history_data, 
            columns=["Record ID", "GPA", "CGPA", "Total Units", "Quality Points", "Academic Term", "Date Saved"]
        )
        
        # Display the main records view (hiding the background database ID)
        st.subheader("Saved Academic Standings")
        st.dataframe(
            df.drop(columns=["Record ID"]), 
            use_container_width=True,
            hide_index=True
        )
        
        st.divider()
        
        # Management panel for deleting specific logs
        st.subheader("Manage Logs")
        with st.expander("Delete an Academic Record"):
            # Create clear drop-down labels combining the saved date and term
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
