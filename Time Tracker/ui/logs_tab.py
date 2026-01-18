import streamlit as st
from core.storage import load_logs, save_logs
import pandas as pd

def show_logs_tab():

    # Load logs
    df = load_logs()
    if df.empty:
        st.info("No logs yet. Start logging activities first!")
        return

    # Initialize session_state for removed ids
    if "removed_ids" not in st.session_state:
        st.session_state.removed_ids = set()

    # Sort newest first
    df_sorted = df.sort_values(by="start_time", ascending=False).reset_index(drop=True)


    for idx, row in df_sorted.iterrows():
        # Skip removed activities
        if row["id"] in st.session_state.removed_ids:
            continue

        total_time = row["duration_seconds"]
        hours = total_time // 3600
        minutes = (total_time % 3600) // 60
        seconds = total_time % 60
        duration_str = f"{hours}h {minutes}m {seconds}s"

        # Unique key for remove button
        remove_key = f"remove_{row['id']}_{idx}"

        with st.container():
            col1, col2 = st.columns([8, 1])
            with col1:
                st.markdown(f"### {row['activity']} — {duration_str}")
                st.markdown(f"*Category: {row['category']} | Mood: {row['mood']}*")
            with col2:
                if st.button("❌", key=remove_key):
                    # Remove immediately
                    st.session_state.removed_ids.add(row["id"])
                    df = df[df["id"] != row["id"]].reset_index(drop=True)
                    save_logs(df)

            st.markdown("---")

    # Download CSV
    csv = df.to_csv(index=False)
    st.download_button("Download Logs CSV", csv, "time_logs.csv", "text/csv")
