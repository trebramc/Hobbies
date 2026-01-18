from datetime import datetime, timedelta
from utils.time_utils import get_period

class Timer:
    """
    Core timer logic.
    Handles start, stop, reset, and elapsed time.
    """

    def __init__(self):
        self.start_time: datetime | None = None
        self.end_time: datetime | None = None
        self.is_running: bool = False

    def start(self):
        """Start the timer."""
        if not self.is_running:
            self.start_time = datetime.now()
            self.end_time = None
            self.is_running = True

    def stop(self):
        """Stop the timer and update elapsed time."""
        if self.is_running:
            self.end_time = datetime.now()
            self.is_running = False

    def reset(self):
        """Reset the timer."""
        self.start_time = None
        self.end_time = timedelta(0)
        self.is_running = False

    def elapsed(self) -> timedelta:
        """
        Return elapsed time as timedelta.
        """
        if self.start_time is None:
            return timedelta(0)

        if self.is_running:
            return datetime.now() - self.start_time

        return self.end_time - self.start_time

    def elapsed_seconds(self) -> int:
        """Elapsed time in seconds."""
        return int(self.elapsed().total_seconds())

    def summary(self) -> dict:
        """
        Return a summary useful for UI or storage.
        """
        if self.start_time is None:
            return {}

        return {
            "start_time": self.start_time,
            "end_time": self.end_time,
            "elapsed_seconds": self.elapsed_seconds(),
            "period": get_period(self.start_time),
            "is_running": self.is_running,
        }