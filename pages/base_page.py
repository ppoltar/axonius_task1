import json
import logging
import allure
from locators.basepage_locators import BasePageLocators

logger = logging.getLogger(__name__)


class BasePage:
    def __init__(self, page):
        self.page = page

    def choose_where_in_search_bar(self, location: str):
        self.page.locator(BasePageLocators.AIRBNB_MAIN_SEARCH_BAR).click()
        self.page.fill(BasePageLocators.AIRBNB_MAIN_SEARCH_LOCATION_INPUT, location)

    def choose_who_in_search_bar(self, who: dict):
        self.page.locator(BasePageLocators.AIRBNB_MAIN_SEARCH_GUESTS).click()
        for guest_type, count in who.items():
            guest_type_selector = BasePageLocators.GUEST_TYPE_INCREASE_SELECTORS.get(guest_type)
            if not guest_type_selector:
                logging.error(f'CanNOT find this guest type: {guest_type}!!! Please check...')
                continue

            for _ in range(count):
                self.page.click(guest_type_selector)

    def click_checkin_date(self):
        self.page.locator(BasePageLocators.AIRBNB_MAIN_SEARCH_CHECKIN_DATE).click()

    def select_date_in_search_bar(self, date: str):
        selector = BasePageLocators.AIRBNB_DATE_BUTTON_BY_DATE.format(date)
        self.page.click(selector)

    def choose_checkin_checkout_date(self, checkin_date: str, checkout_date: str):
        self.click_checkin_date()
        self.select_date_in_search_bar(checkin_date)
        self.select_date_in_search_bar(checkout_date)

    def click_search_button_in_search_bar(self):
        self.page.locator(BasePageLocators.AIRBNB_MAIN_SEARCH_BUTTON).click()

    def location_button(self):
        return self.page.locator(BasePageLocators.AIRBNB_MAIN_SEARCH_LOCATION_BUTTON)

    def date_button(self):
        return self.page.locator(BasePageLocators.AIRBNB_MAIN_SEARCH_DATE_BUTTON)

    def guests_button(self):
        return self.page.locator(BasePageLocators.AIRBNB_MAIN_SEARCH_GUESTS_BUTTON)

    def save_analysis_results(self, place_options_list: list[dict]):
        """
        Save analyzed results to a JSON file and attach it to Allure report.
        """
        logger.info("Saving analyzed results to JSON file and attaching to Allure report.")
        place_options_list_without_locator = [{k: v for k, v in item.items() if k != 'locator'} for item in place_options_list]

        try:
            with self.analysis_file.open("w", encoding="utf-8") as f:
                json.dump(place_options_list_without_locator, f, indent=2)
            logger.debug(f"Results written to {self.analysis_file}")

            with self.analysis_file.open("r", encoding="utf-8") as f:
                allure.attach(
                    f.read(),
                    name="Analyze Results",
                    attachment_type=allure.attachment_type.JSON
                )
            logger.info("Analyze results successfully attached to Allure.")

        except Exception as e:
            logger.error(f"Failed to save or attach analysis results: {e}")
