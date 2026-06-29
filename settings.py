import streamlit as st

def show():
    st.title("⚙️ Settings")

    dark = st.toggle("Dark Theme Mode")
    notify = st.toggle("Enable Calculation Auto-backups")

    if st.button("Save Settings Configuration", use_container_width=True):
        st.success("Configuration preferences updated and saved successfully.")
