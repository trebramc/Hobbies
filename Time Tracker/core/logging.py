from datetime import datetime
import pandas as pd
from core.storage import load_logs, save_logs
from utils.time_utils import get_time_block, get_period


def log_activity(
    activity_name: str,
    category: str,
    mood: str,
    start_time: datetime,
    end_time: datetime,
) -> None:
    """
    Log an activity to the CSV.
    If the activity already exists on the same day, sum the duration.

    Args:
        activity_name (str): Name of the activity
        category (str): Activity category
        mood (str): Mood during activity
        start_time (datetime): Start time
        end_time (datetime): End time
    """

    # Calculate duration
    duration_seconds = int((end_time - start_time).total_seconds())
    start_hour = start_time.hour

    # Load existing logs
    df = load_logs()

    # Extract date/month/year
    date = start_time.date()
    month = start_time.month
    year = start_time.year

    # Check if the activity already exists (same activity name & date)
    mask = (df["activity"] == activity_name) & (df["date"] == pd.to_datetime(date))
    if mask.any():
        # Add duration to existing row
        idx = df.index[mask][0]
        df.at[idx, "duration_seconds"] += duration_seconds
        # Optional: you could update category/mood if you want
    else:
        # Create new row
        new_row = {
            "id": len(df) + 1,
            "start_time": start_time,
            "end_time": end_time,
            "duration_seconds": duration_seconds,
            "activity": activity_name,
            "category": category,
            "mood": mood,
            "start_hour": start_hour,
            "time_block": get_time_block(start_hour),
            "period": get_period(start_hour),
            "date": date,
            "month": month,
            "year": year,
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    # Save updated logs
    save_logs(df)
    