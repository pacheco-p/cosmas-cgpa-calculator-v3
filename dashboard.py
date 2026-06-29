import streamlit as st

def show(get_statistics_func, get_user_func):
    st.title("Dashboard")
    
    user_data = get_user_func(st.session_state.username)
    
    if user_data:
        _, username, _, _, fullname, matric_no, department, current_level = user_data
        
        st.markdown(f"""
        <div style="background-color: #1e293b; padding: 20px; border-radius: 10px; margin-bottom: 25px; border-left: 5px solid #6b21a8;">
            <h3 style="margin-top: 0; color: #ffffff;">Student Academic Profile</h3>
            <table style="width: 100%; border-collapse: collapse; color: #cbd5e1;">
                <tr><td style="padding: 5px 0; font-weight: bold; width: 25%;">Name:</td><td>{fullname}</td></tr>
                <tr><td style="padding: 5px 0; font-weight: bold;">Matric Number:</td><td>{matric_no}</td></tr>
                <tr><td style="padding: 5px 0; font-weight: bold;">Department:</td><td>{department}</td></tr>
                <tr><td style="padding: 5px 0; font-weight: bold;">Current Level:</td><td><span style="background-color: #334155; padding: 2px 8px; border-radius: 4px;">{current_level}</span></td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.write(f"Welcome back, **{st.session_state.username}**!")

    stats = get_statistics_func(st.session_state.username)
    if stats and stats[0] > 0:
        total_calculations, max_cgpa, avg_cgpa = stats
        col1, col2, col3 = st.columns(3)
        col1.metric("Calculations Run", total_calculations)
        col2.metric("Highest CGPA Recorded", f"{max_cgpa:.2f}")
        col3.metric("Average CGPA", f"{avg_cgpa:.2f}")
    else:
        st.info("No calculations stored yet. Head over to the CGPA Calculator tab to run your terms!")
