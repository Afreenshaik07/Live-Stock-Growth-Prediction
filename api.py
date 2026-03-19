import streamlit as st

# ----------------------------
# USERS (Simulation – acceptable for major project)
# ----------------------------
USERS = {
    "field_user": {"password": "field123", "role": "Field User"},
    "manager": {"password": "manager123", "role": "Farm Manager"},
    "analyst": {"password": "admin123", "role": "System Analyst"},
}

st.set_page_config(
    page_title="AgriSense | Livestock Decision Support Platform",
    layout="wide"
)

# ----------------------------
# Session State
# ----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.role = None

# ==================================================
# LOGIN PAGE
# ==================================================
if not st.session_state.logged_in:
    st.title("AgriSense")
    st.subheader("Intelligent Livestock Decision Support Platform")

    st.markdown("---")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in USERS and USERS[username]["password"] == password:
            st.session_state.logged_in = True
            st.session_state.user = username
            st.session_state.role = USERS[username]["role"]
            st.rerun()
        else:
            st.error("Invalid credentials")

    st.info("""
    **Demo Accounts**
    - Field User → field_user / field123  
    - Farm Manager → manager / manager123  
    - System Analyst → analyst / admin123
    """)
    st.stop()

# ==================================================
# SIDEBAR NAVIGATION (REAL-WORLD STYLE)
# ==================================================
st.sidebar.title("AgriSense")
st.sidebar.write(f"User: **{st.session_state.user}**")
st.sidebar.write(f"Role: **{st.session_state.role}**")
st.sidebar.markdown("---")

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.role = None
    st.rerun()

st.sidebar.success("Use the navigation menu to access system modules.")
