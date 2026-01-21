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


