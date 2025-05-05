import re
from datetime import datetime, timedelta
import random

def generate_random_checkin_checkout(min_days_ahead=5, max_days_ahead=30, min_stay=3, max_stay=8):
    """
        Generates random check-in and check-out dates within a specified future range.

        Args:
            min_days_ahead (int): Minimum number of days from today to start check-in.
            max_days_ahead (int): Maximum number of days from today to start check-in.
            min_stay (int): Minimum stay duration in days.
            max_stay (int): Maximum stay duration in days.

        Returns:
            tuple: A tuple containing two `datetime` objects, representing the check-in and check-out dates.
        """
    checkin = datetime.today() + timedelta(days=random.randint(min_days_ahead, max_days_ahead))
    checkout = checkin + timedelta(days=random.randint(min_stay, max_stay))
    return checkin, checkout

def format_date_range(checkin, checkout):
    """
    Formats the check-in and check-out dates into a human-readable string.

    Args:
        checkin (datetime): The check-in date.
        checkout (datetime): The check-out date.

    Returns:
        str: Formatted date range string (e.g., "May 5 – 9" or "May 29 – Jun 2").
    """
    if checkin.month == checkout.month:
        return f"{checkin.strftime('%b')} {checkin.day} – {checkout.day}"
    else:
        return f"{checkin.strftime('%b')} {checkin.day} – {checkout.strftime('%b')} {checkout.day}"


# Generate dynamic dates for the test scenario
checkin_date, checkout_date = generate_random_checkin_checkout()

e2e_test_data = [
    {
        "case": "E2E Test Tel-Aviv reservation 2 adults and 1 child",
        "location": "Tel-Aviv",
        "checkin": checkin_date.strftime("%Y-%m-%d"),
        "checkout": checkout_date.strftime("%Y-%m-%d"),
        "expected_dates": format_date_range(checkin_date, checkout_date),
        "expected_guest": '3 guests',
        "expected_reservation_guests": "2 adults, 1 child",
        "price_ratio": 5,
        "who":  {
            "adults": 2,
            "children": 1
        },
        "checkin_checkout_query": f"check_in={checkin_date.strftime('%Y-%m-%d')}&"
                                  f"check_out={checkout_date.strftime('%Y-%m-%d')}",
    }
]

# Append dynamically generated expected URL pattern to each test case
for test_case in e2e_test_data:
    """
    Constructs a flexible regex pattern that represents the expected structure of the URL 
    containing location, date, and guest parameters.
    """
    url_parts = []

    # Normalize and encode location for URL comparison
    location = test_case["location"]
    if " " in location:
        location = location.replace(" ", "-")
    if "-" in location:
        location = location.replace("-", "~")
    url_parts.append(location)

    # Include date query parameters
    url_parts.append(f"checkin={test_case['checkin']}")
    url_parts.append(f"checkout={test_case['checkout']}")

    # Append guest parameters
    for key, value in test_case["who"].items():
        url_parts.append(f"{key}={value}")

    # Build a regex pattern for URL matching
    pattern = ".*" + ".*".join(url_parts) + ".*"
    test_case["expected_url"] = re.compile(pattern)