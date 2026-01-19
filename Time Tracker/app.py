import streamlit as st

# -------------------------
# Import UI modules
# -------------------------
from ui.timer_tab import show_timer_tab
from ui.logs_tab import show_logs_tab
from ui.analytics_tab import show_analytics_tab

# -------------------------
# Page config
# -------------------------
st.set_page_config(page_title="Time Tracker", layout="wide")

# -------------------------
# Sidebar content
# -------------------------
st.sidebar.markdown(
    "<h1 style='text-align:center;'>⏱ Mindful Tracker</h1>",
    unsafe_allow_html=True
)

st.sidebar.markdown(
    "<p style='text-align:center; font-style: italic;'>Track your flow, capture your mood</p>",
    unsafe_allow_html=True
)

# Flexible whitespace
st.sidebar.markdown("<br><br><br>", unsafe_allow_html=True)

# -------------------------
# Contact info (clean & static)
# -------------------------
st.sidebar.markdown("<hr>", unsafe_allow_html=True)

st.sidebar.markdown(
    "<p style='text-align:center; font-size:12px; margin:0;'>"
    "By <strong>Mc Marbert L. Ordoña</strong>"
    "</p>",
    unsafe_allow_html=True
)

st.sidebar.markdown(
    "<p style='text-align:center; font-size:12px; margin:0;'>"
    "📧 Email for suggestions and improvements:"
    "</p>",
    unsafe_allow_html=True
)

st.sidebar.markdown(
    "<p style='text-align:center; font-size:12px; margin:0;'>"
    "marbertordona24@gmail.com"
    "</p>",
    unsafe_allow_html=True
)

# -------------------------
# Initialize Streamlit session state for timer
# -------------------------
if "start_time" not in st.session_state:
    st.session_state.start_time = None

if "end_time" not in st.session_state:
    st.session_state.end_time = None

# -------------------------
# App layout (tabs only)
# -------------------------
tabs = st.tabs(["Timer", "Logs", "Analytics"])

with tabs[0]:
    show_timer_tab()

with tabs[1]:
    show_logs_tab()

with tabs[2]:
    show_analytics_tab()
