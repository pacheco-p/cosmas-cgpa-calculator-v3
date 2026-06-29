import streamlit as st

def show(get_statistics_func, get_user_func):
    st.title("Dashboard")
    
    user = get_user_func(st.session_state.username)
    
    if user:
        st.markdown(f"""
        <div style="background-color: #1e293b; padding: 20px; border-radius: 10px; margin-bottom: 25px; border-left: 5px solid #6b21a8;">
            <h3 style="margin-top: 0; color: #ffffff; font-family: sans-serif;">Student Academic Profile</h3>
            <table style="width: 100%; border-collapse: collapse; color: #cbd5e1; font-family: sans-serif; font-size: 15px;">
                <tr style="border-bottom: 1px solid #334155;"><td style="padding: 10px 0; font-weight: bold; width: 25%;">Name:</td><td>{user['fullname']}</td></tr>
                <tr style="border-bottom: 1px solid #334155;"><td style="padding: 10px 0; font-weight: bold;">Matric Number:</td><td>{user['matric_no']}</td></tr>
                <tr style="border-bottom: 1px solid #334155;"><td style="padding: 10px 0; font-weight: bold;">Department:</td><td>{user['department']}</td></tr>
                <tr><td style="padding: 10px 0; font-weight: bold;">Current Level:</td><td><span style="background-color: #6b21a8; color: #ffffff; padding: 4px 12px; border-radius: 4px; font-weight: bold;">{user['current_level']}</span></td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.write(f"Welcome back, {st.session_state.username}!")

    stats = get_statistics_func(st.session_state.username)
    if stats and stats[0] > 0:
        total_calculations, max_cgpa, avg_cgpa = stats
        col1, col2, col3 = st.columns(3)
        col1.metric("Calculations Run", total_calculations)
        col2.metric("Highest CGPA Recorded", f"{max_cgpa:.2f}")
        col3.metric("Average CGPA", f"{avg_cgpa:.2f}")
    else:
        st.info("No calculations stored yet. Head over to the CGPA Calculator tab to run your terms!")
