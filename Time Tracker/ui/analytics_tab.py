import streamlit as st
import pandas as pd
import altair as alt
from core.storage import load_logs


def show_analytics_tab():

    st.subheader("Understand your productivity patterns")

    # Load logs
    df = load_logs()
    if df.empty:
        st.info("No logs yet. Start logging activities first!")
        return

    # Ensure datetime
    df['start_time'] = pd.to_datetime(df['start_time'])
    df['end_time'] = pd.to_datetime(df['end_time'])
    df['duration_hours'] = df['duration_seconds'] / 3600

    # -------------------------
    # Filter by timeframe
    # -------------------------
    min_date = df['start_time'].min().date()
    max_date = df['start_time'].max().date()
    start_date, end_date = st.date_input(
        "Select date range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    filtered_df = df[(df['start_time'].dt.date >= start_date) & (df['start_time'].dt.date <= end_date)]

    if filtered_df.empty:
        st.warning("No activities in the selected timeframe.")
        return

    # -------------------------
    # Metrics
    # -------------------------
    total_hours = filtered_df['duration_hours'].sum()
    daily_hours = filtered_df.groupby(filtered_df['start_time'].dt.date)['duration_hours'].sum()
    avg_daily = daily_hours.mean()
    total_sessions = filtered_df.shape[0]
    top_category = filtered_df['category'].mode().iloc[0]
    top_mood = filtered_df['mood'].mode().iloc[0]  # <-- Top Mood metric

    # -------------------------
    # Display metrics
    # -------------------------
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Hours", f"{total_hours:.2f} h")
    col2.metric("Avg Daily Hours", f"{avg_daily:.2f} h")
    col3.metric("Total Sessions", total_sessions)
    col4.metric("Top Category", top_category)
    col5.metric("Top Mood", top_mood)

    st.markdown("---")

    # -------------------------
    # Weekly Bar Graph (hours per weekday)
    # -------------------------
    filtered_df['weekday'] = filtered_df['start_time'].dt.day_name()
    weekly_hours = filtered_df.groupby('weekday')['duration_hours'].sum().reindex(
        ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    ).reset_index()

    st.subheader("How many hours do I spend each day of the week?")
    weekly_chart = alt.Chart(weekly_hours).mark_bar(color="#FFD700").encode(
        x=alt.X('weekday:N', title='Day of Week'),
        y=alt.Y('duration_hours:Q', title='Total Hours'),
        tooltip=['weekday', 'duration_hours']
    ).properties(width=700, height=400)
    st.altair_chart(weekly_chart, use_container_width=True)

    st.markdown("---")


    # -------------------------
    # Mood-Activity-Time Correlation
    # -------------------------
    mood_time = filtered_df.groupby(['start_time', 'activity', 'mood'])['duration_hours'].sum().reset_index()
    mood_time_chart = alt.Chart(mood_time).mark_circle(size=60).encode(
        x=alt.X('start_time:T', title='Date & Time'),
        y=alt.Y('duration_hours:Q', title='Hours'),
        color='mood:N',
        tooltip=['start_time', 'activity', 'mood', 'duration_hours']
    ).properties(width=700, height=400)
    st.subheader("When and during which activity do I feel this mood?")
    st.altair_chart(mood_time_chart, use_container_width=True)

  
 