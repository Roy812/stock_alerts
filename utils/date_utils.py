from datetime import datetime


def format_timestamp_as_date(timestamp: datetime) -> str:
    """Format a datetime as a YYYY-MM-DD string."""
    return timestamp.strftime("%Y-%m-%d")

