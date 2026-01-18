import streamlit as st
from datetime import datetime
from core.timer import Timer
from core.logging import log_activity
from streamlit_autorefresh import st_autorefresh

# -------------------------
# Categories and Moods with emojis
# -------------------------
CATEGORY_OPTIONS = {
    "Work": "💼 Work",
    "Study": "📚 Study",
    "Exercise": "🏋️ Exercise",
    "Leisure": "🎮 Leisure",
    "Chores": "🧹 Chores",
    "Other": "❓ Other"
}

MOOD_OPTIONS = {
    "Focused": "🧠 Focused",
    "Relaxed": "😌 Relaxed",
    "Stressed": "😫 Stressed",
    "Happy": "😄 Happy",
    "Tired": "😴 Tired",
    "Other": "❓ Other"
}

def show_timer_tab():
    # -------------------------
    # Initialize session_state
    # -------------------------
    if "timer" not in st.session_state:
        st.session_state.timer = Timer()
    if "start_time" not in st.session_state:
        st.session_state.start_time = None
    if "end_time" not in st.session_state:
        st.session_state.end_time = None

    timer = st.session_state.timer

    # -------------------------
    # Auto-refresh every 1 second
    # -------------------------
    st_autorefresh(interval=1000, key="timer_autorefresh")

    # -------------------------
    # Custom CSS to remove extra margins
    # -------------------------
    st.markdown(
        """
        <style>
        h1 {
            margin-top: 0px;
            margin-bottom: 5px;
        }
        h2 {
            margin-top: 10px;
        }
        div.stButton > button {
            font-size: 24px;
            padding: 15px 60px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # -------------------------
    # Timer display (left-aligned)
    # -------------------------
    elapsed_td = timer.elapsed()
    elapsed_seconds = int(elapsed_td.total_seconds())
    hours = elapsed_seconds // 3600
    minutes = (elapsed_seconds % 3600) // 60
    seconds = elapsed_seconds % 60

    st.markdown(
        f"<h1 style='font-size:72px; text-align:left;'>{hours:02d}:{minutes:02d}:{seconds:02d}</h1>",
        unsafe_allow_html=True
    )

    # -------------------------
    # Left-aligned toggle button (Start / Stop)
    # -------------------------
    if timer.is_running:
        if st.button("Stop", key="timer_toggle"):
            timer.stop()
            st.session_state.end_time = datetime.now()
    else:
        if st.button("Start", key="timer_toggle"):
            timer.start()
            st.session_state.start_time = datetime.now()
            st.session_state.end_time = None

    # -------------------------
    # Show log input only after stopping
    # -------------------------
    if st.session_state.end_time is not None:
        st.subheader("Log Activity")

        activity_name = st.text_input("Activity Name")

        # Category selectbox with emojis
        category_label = st.selectbox("Category", list(CATEGORY_OPTIONS.values()))
        category = [k for k, v in CATEGORY_OPTIONS.items() if v == category_label][0]
        if category == "Other":
            category = st.text_input("Enter custom category")

        # Mood selectbox with emojis
        mood_label = st.selectbox("Mood", list(MOOD_OPTIONS.values()))
        mood = [k for k, v in MOOD_OPTIONS.items() if v == mood_label][0]
        if mood == "Other":
            mood = st.text_input("Enter custom mood")

        if st.button("Save Activity"):
            start_time = st.session_state.start_time
            end_time = st.session_state.end_time

            if not activity_name:
                st.error("Please enter an activity name.")
            elif start_time is None:
                st.error("Start the timer first!")
            else:
                log_activity(activity_name, category, mood, start_time, end_time)
                st.success(f"Activity '{activity_name}' logged!")
                timer.reset()
                st.session_state.start_time = None
                st.session_state.end_time = None

