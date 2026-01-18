from pathlib import Path
import pandas as pd

# ============================
# File & schema configuration
# ============================

DATA_DIR = Path("data")
DATA_FILE = DATA_DIR / "time_logs.csv"

COLUMNS = [
    "id",
    "start_time",
    "end_time",
    "duration_seconds",

    "activity",
    "category",
    "mood",

    "start_hour",
    "time_block",
    "period",

    "date",
    "month",
    "year",
]

# ============================
# Core storage functions
# ============================

def ensure_data_file() -> None:
    """
    Ensure that the data directory and CSV file exist.
    If the CSV does not exist, create it with the correct columns.
    """
    DATA_DIR.mkdir(exist_ok=True)

    if not DATA_FILE.exists():
        empty_df = pd.DataFrame(columns=COLUMNS)
        empty_df.to_csv(DATA_FILE, index=False)


def load_logs() -> pd.DataFrame:
    """
    Load time logs from the CSV.

    Returns:
        pd.DataFrame: All logged timer records
    """
    ensure_data_file()

    df = pd.read_csv(
        DATA_FILE,
        parse_dates=["start_time", "end_time"]
    )

    return df


def save_logs(df: pd.DataFrame) -> None:
    """
    Save logs to CSV.

    Args:
        df (pd.DataFrame): The full logs DataFrame to persist
    """
    ensure_data_file()
    df.to_csv(DATA_FILE, index=False)

