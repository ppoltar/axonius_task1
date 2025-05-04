import re
import allure
import pytest
import logging
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

    airbnb_page.choose_where_in_search_bar(test_data['location'])
    airbnb_page.choose_who_in_search_bar(test_data['who'])
    airbnb_page.click_search_button_in_search_bar()


    logger.info(f"Validate search params by url.")
    expect(page).to_have_url(test_data["expected_url"])
    pass

