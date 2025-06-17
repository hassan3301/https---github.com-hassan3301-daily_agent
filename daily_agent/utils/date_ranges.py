from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta

def get_named_date_ranges(today: date = None):
    """Returns a dictionary of commonly used date ranges based on today's date."""
    today = today or date.today()
    first_day_this_month = today.replace(day=1)
    first_day_last_month = first_day_this_month - relativedelta(months=1)
    first_day_next_month = first_day_this_month + relativedelta(months=1)

    start_of_week = today - timedelta(days=today.weekday())  # Monday
    start_of_last_week = start_of_week - timedelta(weeks=1)

    quarter = (today.month - 1) // 3 + 1
    first_day_this_quarter = date(today.year, 3 * (quarter - 1) + 1, 1)
    first_day_last_quarter = first_day_this_quarter - relativedelta(months=3)

    return {
        "today": {
            "start": today.isoformat(),
            "end": (today + timedelta(days=1)).isoformat(),
        },
        "this_week": {
            "start": start_of_week.isoformat(),
            "end": (start_of_week + timedelta(days=7)).isoformat(),
        },
        "last_week": {
            "start": start_of_last_week.isoformat(),
            "end": start_of_week.isoformat(),
        },
        "this_month": {
            "start": first_day_this_month.isoformat(),
            "end": first_day_next_month.isoformat(),
        },
        "last_month": {
            "start": first_day_last_month.isoformat(),
            "end": first_day_this_month.isoformat(),
        },
        "this_quarter": {
            "start": first_day_this_quarter.isoformat(),
            "end": (first_day_this_quarter + relativedelta(months=3)).isoformat(),
        },
        "last_quarter": {
            "start": first_day_last_quarter.isoformat(),
            "end": first_day_this_quarter.isoformat(),
        }
    }
