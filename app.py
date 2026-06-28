import streamlit as st
import auth,dashboard,calculator,history,profile

st.set_page_config(page_title="Cosmas CGPA Calculator",page_icon="🎓",layout="wide")

st.session_state.setdefault("logged_in",False)
st.session_state.setdefault("username","")

if not st.session_state.logged_in:
    st.title("🎓 Cosmas CGPA Calculator")
    t1,t2=st.tabs(["Login","Create Account"])
    with t1:
        u=st.text_input("Username")
        p=st.text_input("Password",type="password")
        if st.button("Login"):
            if auth.login(u,p):
                st.session_state.logged_in=True
                st.session_state.username=u
                st.rerun()
            st.error("Invalid username or password.")
    with t2:
        su=st.text_input("New Username")
        se=st.text_input("Email")
        sp=st.text_input("Password",type="password")
        cp=st.text_input("Confirm Password",type="password")
        if st.button("Create Account"):
            if sp!=cp:
                st.error("Passwords do not match.")
            else:
                ok,msg=auth.register(su,se,sp)
                (st.success if ok else st.error)(msg)
else:
    st.sidebar.success(f"Welcome, {st.session_state.username}")
    page=st.sidebar.radio("Navigation",["Dashboard","CGPA Calculator","History","Profile"])
    if st.sidebar.button("Logout"):
        st.session_state.logged_in=False
        st.session_state.username=""
        st.rerun()
    if page=="Dashboard":
        dashboard.show()
    elif page=="CGPA Calculator":
        calculator.show()
    elif page=="History":
        history.show()
    else:
        profile.show()