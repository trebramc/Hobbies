import streamlit as st
from core.storage import load_logs

# ============================
# Session state initialization
# ============================

def init_state() -> None:
    """
    Initialize all required Streamlit session_state variables.
    This function is safe to call on every rerun
    """

    # Persistent_data (loaded from CSV once per session)
    if "logs" not in st.session_state:
        st.session_state.logs = load_logs()
    
    # Timer state

    if "timer_running" not in st.session_state:
        st.session_state.timer_running = False
    
    if "start_time" not in st.session_state:
        st.session_state.start_time = None
    
    # Temporary record after stopping timer

    if "last_record" not in st.session_state:
        st.session_state.last_record = None
    