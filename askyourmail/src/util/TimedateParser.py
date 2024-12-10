import dateparser
from datetime import datetime, timedelta
import re

def parse_date_range(query):
    # Special handling for "Nth week of Month Year"
    if "week" in query.lower():
        # Extract the week number and month/year
        match = re.match(r"(\d+)[a-z]{2} week of (.+)", query.lower())
        if match:
            week_number = int(match.group(1))
            month_year = match.group(2).strip()
            # Parse the first day of the month
            first_day_of_month = dateparser.parse(month_year).replace(day=1)
            # Calculate the start of the Nth week
            start_of_week = first_day_of_month + timedelta(days=(week_number - 1) * 7)
            # Adjust if the first day of the month is not a Monday
            start_of_week -= timedelta(days=start_of_week.weekday())
            # Calculate the end of the week
            end_of_week = start_of_week + timedelta(days=6, hours=23, minutes=59, seconds=59)
            return start_of_week, end_of_week

    parsed_date = dateparser.parse(query)
    if not parsed_date:
        raise ValueError(f"Could not parse query: {query}")

    # Handle queries like "2001" (Year only)
    if query.strip().isdigit() and len(query.strip()) == 4:
        year = int(query.strip())
        start_date = datetime(year, 1, 1, 0, 0, 0)  # January 1st, 00:00:00
        end_date = datetime(year, 12, 31, 23, 59, 59)  # December 31st, 23:59:59
        return start_date, end_date

    # Handle queries like "April 2000"
    if re.match(r".+\d{4}$", query):
        start_date = parsed_date.replace(day=1, hour=0, minute=0, second=0)
        next_month = (start_date.replace(day=28) + timedelta(days=4))  # Move to the next month
        end_date = next_month.replace(day=1) - timedelta(seconds=1)
        return start_date, end_date

    # Determine if it's a specific day
    start_date = parsed_date.replace(hour=0, minute=0, second=0)
    end_date = parsed_date.replace(hour=23, minute=59, second=59)
    return start_date, end_date
