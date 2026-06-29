import streamlit as st
import pandas as pd

def show(get_history_func, delete_history_func):
    try:
        st.image("assets/cosmas_banner.png", use_container_width=True)
    except:
        st.markdown("""
        <div style="background: linear-gradient(90deg, #1e3a8a 0%, #0f172a 100%); padding: 30px; border-radius: 10px; text-align: center; margin-bottom: 20px;">
            <h1 style="color: white; margin: 0; font-family: sans-serif; letter-spacing: 2px;">COSMAS AT SUG TOP SEAT</h1>
            <p style="color: #cbd5e1; margin: 5px 0 0 0; font-family: sans-serif;">Support • Pray • Canvass</p>
        </div>
        """, unsafe_allow_html=True)

    st.title("Calculation History Log")
    st.markdown("Review and manage your previously saved GPA and CGPA computation records.")

    records = get_history_func(st.session_state.username)

    if records:
        df = pd.DataFrame(
            records, 
            columns=["ID", "GPA", "CGPA", "Total Units", "Quality Points", "Semester Label", "Date Saved"]
        )
        st.dataframe(df.drop(columns=["ID"]), use_container_width=True, hide_index=True)
        
        st.divider()
        st.subheader("Manage Records")
        
        record_options = {f"{row[5]} (CGPA: {row[2]:.2f}) - {row[6]}": row[0] for row in records}
        selected_record = st.selectbox("Select a calculation record to delete:", list(record_options.keys()))
        
        if st.button("Delete Selected Record", type="primary"):
            record_id = record_options[selected_record]
            delete_history_func(record_id)
            st.success("Record deleted successfully!")
            st.rerun()
    else:
        st.info("No saved computation history found. Go to the CGPA Calculator to save your logs.")
