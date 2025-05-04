import logging
from playwright.sync_api import Page
from locators.airbnb_locators import AirbnbLocators

logger = logging.getLogger(__name__)

class AirbnbPage:
    def __init__(self, page: Page):
        self.page = page

    def go_to_airbnb_page(self):
        """
        """
        try:
            self.page.goto(AirbnbLocators.AIRBNB_URL)
            self.page.locator(AirbnbLocators.AIRBNB_MAIN_SEARCH_BAR).wait_for(state="visible")
        except Exception as e:
            error_message = f"Failed to go to the page: {AirbnbLocators.AIRBNB_URL}. Error: {str(e)}"
            logger.error(error_message)
            raise Exception(f"Page navigation failed: {error_message}")

    def choose_where_in_search_bar(self, location: str):
        self.page.locator(AirbnbLocators.AIRBNB_MAIN_SEARCH_BAR).click()
        self.page.fill(AirbnbLocators.AIRBNB_MAIN_SEARCH_LOCATION_INPUT, location)

    def choose_who_in_search_bar(self, who: dict):
        self.page.locator(AirbnbLocators.AIRBNB_MAIN_SEARCH_GUESTS).click()
        for guest_type, count in who.items():
            guest_type_selector = AirbnbLocators.GUEST_TYPE_INCREASE_SELECTORS.get(guest_type)
            if not guest_type_selector:
                logging.error(f'CanNOT find this guest type: {guest_type}!!! Please check...')
                continue

            for _ in range(count):
                self.page.click(guest_type_selector)

    def click_search_button_in_search_bar(self):
        self.page.locator(AirbnbLocators.AIRBNB_MAIN_SEARCH_BUTTON).click()

