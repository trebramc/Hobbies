import streamlit as st
from datetime import datetime

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
st.sidebar.markdown("<h1 style='text-align:center;'>⏱ Mindful Tracker</h1>", unsafe_allow_html=True)
st.sidebar.markdown(
    "<p style='text-align:center; font-style: italic;'>Track your flow, capture your mood </p>",
    unsafe_allow_html=True
)

# Flexible whitespace
st.sidebar.markdown("<br><br><br>", unsafe_allow_html=True)

# Contact info (smaller and centered)
st.sidebar.markdown("<hr>", unsafe_allow_html=True)
st.sidebar.markdown(
    "<p style='text-align:center; font-size:12px; margin:0;'>By <strong>Mc Marbert L. Ordoña</strong></p>",
    unsafe_allow_html=True
)
st.sidebar.markdown(
    "<p style='text-align:center; font-size:12px; margin:0;'>📧 marbertordona24@gmail.com</p>",
    unsafe_allow_html=True
)

# -------------------------
# Feedback form at bottom (toggle)
# -------------------------
if "show_feedback" not in st.session_state:
    st.session_state.show_feedback = False
if "feedback_text" not in st.session_state:
    st.session_state.feedback_text = ""

# Toggle feedback form
if st.sidebar.button("💬 Give Feedback"):
    st.session_state.show_feedback = not st.session_state.show_feedback  # toggle True/False

# Only show form if toggled
if st.session_state.show_feedback:
    st.sidebar.subheader("Your Feedback")
    st.session_state.feedback_text = st.sidebar.text_area(
        "Your feedback or suggestions:",
        value=st.session_state.feedback_text
    )

    if st.sidebar.button("Submit Feedback"):
        if st.session_state.feedback_text.strip():
            # Save feedback with timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open("ui/feedback.txt", "a") as f:
                f.write(f"[{timestamp}] {st.session_state.feedback_text}\n\n")

            st.sidebar.success("Thanks for your feedback!")
            st.session_state.feedback_text = ""  # Clear textarea
            st.session_state.show_feedback = False  # hide form again
        else:
            st.sidebar.error("Please enter some feedback before submitting.")

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
