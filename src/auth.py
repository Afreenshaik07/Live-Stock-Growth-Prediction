import streamlit as st

def init_session():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "user" not in st.session_state:
        st.session_state.user = None
    if "role" not in st.session_state:
        st.session_state.role = None

def require_login(required_role=None):
    init_session()

    if not st.session_state.logged_in:
        st.warning("Please login to continue.")
        st.stop()

    if required_role and st.session_state.role != required_role:
        st.error("Access denied for this role.")
        st.stop()
