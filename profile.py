import streamlit as st

def show(get_user_func):
    st.title("My Profile")
    
    # Fetch full account data matrix from core controller
    user_data = get_user_func(st.session_state.username)
    
    if user_data:
        _, username, email, _, fullname, matric_no, department, current_level = user_data
        
        # Main Display Columns separating Account Profile info from Institutional Context
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Personal Information")
            st.markdown(f"""
            * **Full Name:** {fullname}
            * **Username:** {username}
            * **Email Address:** {email}
            """)
            
        with col2:
            st.subheader("Institutional Details")
            st.markdown(f"""
            * **Matriculation Number:** {matric_no}
            * **Academic Department:** {department}
            * **Current Level Standing:** {current_level}
            """)
            
        st.divider()
        st.caption("To update registration parameters or alter account credentials, please use the Settings workspace module.")
    else:
        st.error("Failed to compile user account profile metrics. Please log out and authenticate back in.")
