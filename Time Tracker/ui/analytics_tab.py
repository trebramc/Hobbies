import streamlit as st
import pandas as pd
import altair as alt
from core.storage import load_logs


def show_analytics_tab():

    st.subheader("Understand your productivity patterns")

    # -------------------------
    # Load logs
    # -------------------------
    df = load_logs()
    if df.empty:
        st.info("No logs yet. Start logging activities first!")
        return

    # -------------------------
    # Datetime handling (CRITICAL FIX)
    # -------------------------
    df['start_time'] = pd.to_datetime(df['start_time'], utc=True)
    df['end_time'] = pd.to_datetime(df['end_time'], utc=True)

    df['duration_hours'] = df['duration_seconds'] / 3600

    # Convert UTC → Asia/Manila, then remove tz for Altair
    df['start_time_local'] = (
        df['start_time']
        .dt.tz_convert('Asia/Manila')
        .dt.tz_localize(None)
    )

    # -------------------------
    # Filter by timeframe
    # -------------------------
    min_date = df['start_time_local'].min().date()
    max_date = df['start_time_local'].max().date()

    start_date, end_date = st.date_input(
        "Select date range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    filtered_df = df[
        (df['start_time_local'].dt.date >= start_date) &
        (df['start_time_local'].dt.date <= end_date)
    ]

    if filtered_df.empty:
        st.warning("No activities in the selected timeframe.")
        return

    # -------------------------
    # Metrics
    # -------------------------
    total_hours = filtered_df['duration_hours'].sum()

    daily_hours = (
        filtered_df
        .groupby(filtered_df['start_time_local'].dt.date)['duration_hours']
        .sum()
    )
    avg_daily = daily_hours.mean()

    total_sessions = len(filtered_df)

    top_category = (
        filtered_df['category'].mode().iloc[0]
        if not filtered_df['category'].dropna().empty else "N/A"
    )

    top_mood = (
        filtered_df['mood'].mode().iloc[0]
        if not filtered_df['mood'].dropna().empty else "N/A"
    )

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
    # Weekly Bar Graph
    # -------------------------
    filtered_df['weekday'] = filtered_df['start_time_local'].dt.day_name()

    weekday_order = [
        'Monday', 'Tuesday', 'Wednesday',
        'Thursday', 'Friday', 'Saturday', 'Sunday'
    ]

    weekly_hours = (
        filtered_df
        .groupby('weekday')['duration_hours']
        .sum()
        .reindex(weekday_order, fill_value=0)
        .reset_index()
    )

    st.subheader("How much time do I spend on each day of the week?")
    weekly_chart = alt.Chart(weekly_hours).mark_bar(color="#FFD700").encode(
        x=alt.X('weekday:N', sort=weekday_order, title='Day of Week'),
        y=alt.Y('duration_hours:Q', title='Total Hours'),
        tooltip=[
            alt.Tooltip('weekday:N', title='Day'),
            alt.Tooltip('duration_hours:Q', title='Hours', format='.2f')
        ]
    ).properties(height=400)

    st.altair_chart(weekly_chart, use_container_width=True)

    st.markdown("---")

   # -------------------------
    # Mood–Activity–Time Correlation (24-hour, date-independent, exact time)
    # -------------------------
    
    # Exact time of day as continuous float (0–24)
    filtered_df['hour_float'] = (
        filtered_df['start_time_local'].dt.hour +
        filtered_df['start_time_local'].dt.minute / 60 +
        filtered_df['start_time_local'].dt.second / 3600
    )
    
    mood_time = (
        filtered_df
        .groupby(['hour_float', 'activity', 'mood'], as_index=False)['duration_hours']
        .sum()
    )
    
    mood_time_chart = (
        alt.Chart(mood_time)
        .mark_circle(size=70, opacity=0.7)
        .encode(
            x=alt.X(
                'hour_float:Q',
                title='What time of day does this usually happen?',
                scale=alt.Scale(domain=[0, 24], nice=False),
                axis=alt.Axis(
                    tickCount=24,
                    values=list(range(0, 25)),
                    labelExpr="""
                        datum.value == 0 ? '12 AM' :
                        datum.value < 12 ? datum.value + ' AM' :
                        datum.value == 12 ? '12 PM' :
                        (datum.value - 12) + ' PM'
                    """
                )
            ),
            y=alt.Y(
                'duration_hours:Q',
                title='How long did it last? (hours)'
            ),
            color=alt.Color(
                'mood:N',
                legend=alt.Legend(title="Mood")
            ),
            tooltip=[
                alt.Tooltip('activity:N', title='Activity'),
                alt.Tooltip('mood:N', title='Mood'),
                alt.Tooltip('duration_hours:Q', title='Hours', format='.2f'),
                alt.Tooltip(
                    'hour_float:Q',
                    title='Exact Time',
                    format='.2f'
                )
            ]
        )
        .properties(height=400)
    )
    
    st.subheader("🕒 When during the day do I feel and perform this way?")
    st.altair_chart(mood_time_chart, use_container_width=True)



