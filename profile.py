import streamlit as st

def show(get_user_profile_func, update_user_profile_func):
    try:
        st.image("assets/cosmas_banner.png", use_container_width=True)
    except:
        st.markdown("""
        <div style="background: linear-gradient(90deg, #1e3a8a 0%, #0f172a 100%); padding: 30px; border-radius: 10px; text-align: center; margin-bottom: 20px;">
            <h1 style="color: white; margin: 0; font-family: sans-serif; letter-spacing: 2px;">COSMAS AT SUG TOP SEAT</h1>
            <p style="color: #cbd5e1; margin: 5px 0 0 0; font-family: sans-serif;">Support • Pray • Canvass</p>
        </div>
        """, unsafe_allow_html=True)

    st.title("My Profile Settings")
    st.markdown("Manage your institutional user records and tracking configurations.")

    user_data = get_user_profile_func(st.session_state.username)

    if user_data:
        with st.form("profile_form", clear_on_submit=False):
            st.subheader("Personal Identification")
            fullname = st.text_input("Full Name", value=user_data.get('fullname', ''))
            email = st.text_input("Email Address", value=user_data.get('email', ''))
            
            st.subheader("Academic Information")
            matric_no = st.text_input("Matric Number", value=user_data.get('matric_no', ''))
            department = st.text_input("Department", value=user_data.get('department', ''))
            
            levels = ["100L", "200L", "300L", "400L", "500L"]
            current_level = user_data.get('current_level', '100L')
            level_idx = levels.index(current_level) if current_level in levels else 0
            level = st.selectbox("Current Academic Level", levels, index=level_idx)
            
            save_changes = st.form_submit_button("Update Settings Profile")
            
            if save_changes:
                if fullname.strip() and department.strip() and matric_no.strip():
                    success = update_user_profile_func(
                        st.session_state.username,
                        fullname,
                        email,
                        matric_no,
                        department,
                        level
                    )
                    if success:
                        st.success("Your profile settings have been successfully updated!")
                        st.rerun()
                    else:
                        st.error("An error occurred while updating your database profile entry.")
                else:
                    st.error("Name, Matric Number, and Department cannot be left blank.")
