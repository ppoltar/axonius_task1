import re
from datetime import datetime, timedelta
import random

def generate_random_checkin_checkout(min_days_ahead=5, max_days_ahead=30, min_stay=3, max_stay=8):
    checkin = datetime.today() + timedelta(days=random.randint(min_days_ahead, max_days_ahead))
    checkout = checkin + timedelta(days=random.randint(min_stay, max_stay))
    return checkin, checkout

def format_date_range(checkin, checkout):
    if checkin.month == checkout.month:
        return f"{checkin.strftime('%b')} {checkin.day} – {checkout.day}"
    else:
        return f"{checkin.strftime('%b')} {checkin.day} – {checkout.strftime('%b')} {checkout.day}"


# random dates
checkin_date, checkout_date = generate_random_checkin_checkout()

e2e_test_data = [
    {
        "case": "E2E Test Tel-Aviv reservation 2 adults and child",
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

# Add dynamic expected_url to each test case
for test_case in e2e_test_data:
    url_parts = []

    # Add location
    location = test_case["location"]
    if " " in location:
        location = location.replace(" ", "-")
    if "-" in location:
        location = location.replace("-", "~")
    url_parts.append(location)

    # Add check-in and check-out dates
    url_parts.append(f"checkin={test_case['checkin']}")
    url_parts.append(f"checkout={test_case['checkout']}")

    # Add guests
    for key, value in test_case["who"].items():
        url_parts.append(f"{key}={value}")

    # Create regex pattern
    pattern = ".*" + ".*".join(url_parts) + ".*"
    test_case["expected_url"] = re.compile(pattern)