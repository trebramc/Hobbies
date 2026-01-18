# =================================
# Time-of-day helper functions
# =================================

def get_time_block(hour: int) -> str:
    """
    Convert an hour (0-23) into a detailed time block.
    """
    if 5 <= hour < 9:        
        return "Early Morning"
    elif 9 <= hour < 12:
        return "Late Morning"
    elif 12 <= hour < 17:
        return "Afternoon"
    elif 17 <= hour < 21:
        return "Evening"
    else:
        return "Night"

def get_period(hour: int) -> str:
    """
    Convert an hour (0-23) into a broad time period.
    """
    return "AM" if hour < 12 else "PM"