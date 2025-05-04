import allure
import pytest
import logging
import json
from pathlib import Path
from tests.e2e_data import e2e_test_data
from pages.airbnb_page import AirbnbPage
from playwright.sync_api import expect

logger = logging.getLogger(__name__)

@allure.description("""
""")

@pytest.mark.e2e
@pytest.mark.parametrize("test_data", e2e_test_data, ids=[data["case"] for data in e2e_test_data])
def test_e2e(page, test_data):
    logger.info(f"Starting test: {test_data['case']}.")
    airbnb_page = AirbnbPage(page)
    airbnb_page.go_to_airbnb_page()

    logger.info(f"Choosing location, dates and guest.")
    airbnb_page.choose_where_in_search_bar(test_data['location'])
    airbnb_page.choose_checkin_checkout_date(test_data['checkin'], test_data['checkout'])
    airbnb_page.choose_who_in_search_bar(test_data['who'])
    airbnb_page.click_search_button_in_search_bar()


    logger.info(f"Validate search params by url.")
    expect(airbnb_page.page).to_have_url(test_data["expected_url"])

    logger.info(f"Validate search params by ui.")
    expect(airbnb_page.location_button()).to_have_text(test_data['location'])
    expect(airbnb_page.date_button()).to_have_text(test_data['expected_dates'])
    expect(airbnb_page.guests_button()).to_have_text(test_data['expected_guest'])

    logger.info(f'Find this sorted option by rating and price')
    options = airbnb_page.options_results_sorted_by_rating_price()
    options_list_without_locator = [{k: v for k, v in item.items() if k != 'locator'} for item in options]

    logger.info(f'Saving the analyze results to file and attached to allure report')
    output_path = Path("reports") / "analyze_results.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(options_list_without_locator, f, indent=2)

    with open(output_path, "r", encoding="utf-8") as f:
        allure.attach(f.read(), name="Analyze Results", attachment_type=allure.attachment_type.JSON)

    pass

