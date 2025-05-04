import re
from urllib.parse import quote

e2e_test_data = [
    {
        "case": "E2E Test Tel-Aviv reservation 2 adults and child",
        "location": "Tel-Aviv",
        "who":  {
            "adults": 2,
            "children": 1
            },
    }
]

# Add dynamic expected_url to each test case
for test_case in e2e_test_data:
    url_parts = []

    # Add encoded location string (e.g., Tel-Aviv -> Tel-Aviv or Tel%20Aviv)
    if "location" in test_case:
        location = test_case["location"]

        # Only replace if present
        if " " in location:
            location = location.replace(" ", "-")
        if "-" in location:
            location = location.replace("-", "~")

        # Add query= encoded formatted location
        url_parts.append(location)

    # Add guest params
    for key, value in test_case["who"].items():
        url_parts.append(f"{key}={value}")

    # Create regex pattern
    pattern = ".*" + ".*".join(url_parts) + ".*"
    test_case["expected_url"] = re.compile(pattern)