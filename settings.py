import streamlit as st

def show():

    st.title("⚙️ Settings")

    dark = st.toggle("Dark Mode")

    notify = st.toggle("Enable Notifications")

    if st.button("Save Settings"):

        st.success("Settings Saved")