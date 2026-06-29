import streamlit as st

def show(get_user_func):
    st.title("My Profile")
    
    user = get_user_func(st.session_state.username)
    
    if user:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Personal Information")
            st.markdown(f"""
            * **Full Name:** {user['fullname']}
            * **Username:** {user['username']}
            * **Email Address:** {user['email']}
            """)
            
        with col2:
            st.subheader("Institutional Details")
            st.markdown(f"""
            * **Matriculation Number:** {user['matric_no']}
            * **Academic Department:** {user['department']}
            * **Current Level Standing:** {user['current_level']}
            """)
            
        st.divider()
        st.caption("To update registration parameters or alter account credentials, please use the Settings workspace module.")
    else:
        st.error("Failed to compile user account profile metrics. Please log out and authenticate back in.")
