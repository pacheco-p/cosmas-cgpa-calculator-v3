import streamlit as st

def show(get_user_func, update_user_func=None):
    st.title("My Profile Workspace")
    user = get_user_func(st.session_state.username)
    
    if user:
        view_tab, edit_tab = st.tabs(["📋 View Registration Details", "⚙️ Edit Profile / Fix Mistakes"])
        
        with view_tab:
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Personal Metadata")
                st.markdown(f"""
                * **Full Identity Name:** {user['fullname']}
                * **System Account Handle:** {user['username']}
                * **Primary Email Connection:** {user['email']}
                """)
            with col2:
                st.subheader("Institutional Affiliation Parameters")
                st.markdown(f"""
                * **Matriculation Reference Number:** {user['matric_no']}
                * **Department / Faculty:** {user['department']}
                * **Current Status Milestone:** {user['current_level']}
                """)
                
        with edit_tab:
            st.subheader("Correct Registration Metadata Mistakes")
            st.write("Modify details below to fix typos instantly across the dashboard system.")
            
            with st.form("edit_profile_form"):
                new_fullname = st.text_input("Full Identity Name", value=user['fullname'])
                new_email = st.text_input("Primary Email Connection", value=user['email'])
                new_matric_no = st.text_input("Matriculation Reference Number", value=user['matric_no'])
                new_department = st.text_input("Department / Faculty", value=user['department'])
                new_level = st.selectbox(
                    "Current Status Milestone", 
                    ["100L", "200L", "300L", "400L", "500L"], 
                    index=["100L", "200L", "300L", "400L", "500L"].index(user['current_level']) if user['current_level'] in ["100L", "200L", "300L", "400L", "500L"] else 0
                )
                
                submit_btn = st.form_submit_button("Save Alterations & Synchronize System Panels", use_container_width=True)
                
                if submit_btn:
                    if update_user_func:
                        success = update_user_func(
                            username=user['username'], fullname=new_fullname, email=new_email,
                            matric_no=new_matric_no, department=new_department, current_level=new_level
                        )
                        if success:
                            st.success("Profile saved and dashboard synced successfully!")
                            st.rerun()
                        else:
                            st.error("Encountered database commit error writing updates.")
                    else:
                        st.warning("Update process handler functions are unavailable.")
