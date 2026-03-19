import streamlit as st
from src.auth import init_session

USERS = {
    "farmer": {"password": "farmer123", "role": "Farmer"},
    "admin": {"password": "admin123", "role": "Admin"},
}

st.set_page_config(
    page_title="Livestock Growth Decision Support System",
    layout="wide"
)

init_session()

# ---------- LOGIN ----------
if not st.session_state.logged_in:
    st.title("Livestock Growth Decision Support System")
    st.caption("Machine-Learning based productivity intelligence")

    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        if user in USERS and USERS[user]["password"] == pwd:
            st.session_state.logged_in = True
            st.session_state.user = user
            st.session_state.role = USERS[user]["role"]
            st.rerun()
        else:
            st.error("Invalid credentials")

    st.info("""
    Demo Users  
    • Farmer → farmer / farmer123  
    • Admin → admin / admin123
    """)
    st.stop()

# ---------- SIDEBAR ----------
st.sidebar.title("Navigation")
st.sidebar.write(f"User: **{st.session_state.user}**")
st.sidebar.write(f"Role: **{st.session_state.role}**")

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.role = None
    st.rerun()
