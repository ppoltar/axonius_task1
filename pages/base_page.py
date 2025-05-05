import json
import logging
import allure
from locators.basepage_locators import BasePageLocators
from pathlib import Path

logger = logging.getLogger(__name__)


class BasePage:
    """
    Base page object model providing shared interactions for Airbnb's main functionality.
    """
    def __init__(self, page):
        """
        Initializes the BasePage with a Playwright page instance.

        Args:
            page (playwright.sync_api.Page): The Playwright page object used for browser interaction.
        """
        self.page = page

    def choose_where_in_search_bar(self, location: str):
        """
          Fills in the 'Where' field in the Airbnb search bar.

          Args:
              location (str): The desired location to search for.
          """
        self.page.locator(BasePageLocators.AIRBNB_MAIN_SEARCH_BAR).click()
        self.page.fill(BasePageLocators.AIRBNB_MAIN_SEARCH_LOCATION_INPUT, location)

    def choose_who_in_search_bar(self, who: dict):
        """
        Fills in the 'Who' section by selecting the number of guests.

        Args:
            who (dict): A dictionary specifying guest types and counts, e.g., {"adults": 2, "children": 1}.
        """
        self.page.locator(BasePageLocators.AIRBNB_MAIN_SEARCH_GUESTS).click()
        for guest_type, count in who.items():
            guest_type_selector = BasePageLocators.GUEST_TYPE_INCREASE_SELECTORS.get(guest_type)
            if not guest_type_selector:
                logging.error(f'CanNOT find this guest type: {guest_type}!!! Please check...')
                continue

            for _ in range(count):
                self.page.click(guest_type_selector)

    def click_checkin_date(self):
        """
        Clicks the check-in date field to open the calendar widget.
        """
        self.page.locator(BasePageLocators.AIRBNB_MAIN_SEARCH_CHECKIN_DATE).click()

    def select_date_in_search_bar(self, date: str):
        """
        Selects a specific date from the calendar widget.

        Args:
            date (str): The date string in the format used by the locator, e.g., "2025-05-10".
        """
        selector = BasePageLocators.AIRBNB_DATE_BUTTON_BY_DATE.format(date)
        self.page.click(selector)

    def choose_checkin_checkout_date(self, checkin_date: str, checkout_date: str):
        """
        Selects both check-in and check-out dates using the calendar widget.

        Args:
            checkin_date (str): Check-in date in the expected format.
            checkout_date (str): Check-out date in the expected format.
        """
        self.click_checkin_date()
        self.select_date_in_search_bar(checkin_date)
        self.select_date_in_search_bar(checkout_date)

    def click_search_button_in_search_bar(self):
        """
        Clicks the search button to initiate the Airbnb search with provided filters.
        """
        self.page.locator(BasePageLocators.AIRBNB_MAIN_SEARCH_BUTTON).click()

    def location_button(self):
        """
        Returns:
            Locator: Locator object for the search result's location button.
        """
        return self.page.locator(BasePageLocators.AIRBNB_MAIN_SEARCH_LOCATION_BUTTON)

    def date_button(self):
        """
        Returns:
            Locator: Locator object for the search result's date button.
        """
        return self.page.locator(BasePageLocators.AIRBNB_MAIN_SEARCH_DATE_BUTTON)

    def guests_button(self):
        """
        Returns:
            Locator: Locator object for the search result's guest button.
        """
        return self.page.locator(BasePageLocators.AIRBNB_MAIN_SEARCH_GUESTS_BUTTON)

    def save_attach_results(self, options_list: list[dict], filename: str):
        """
        Saves filtered search results to a JSON file and attaches them to the Allure report.

        Args:
            options_list (list[dict]): List of dictionaries containing property data (e.g., name, price, rating).
            filename (str): Name of the JSON file to save results to.

        This method excludes locator objects before saving and supports Allure integration.

        Raises:
            Exception: If saving to the file or attaching to the Allure report fails.
    """
        logger.info("Saving results to JSON file and attaching to Allure report.")
        options_list_without_locator = [{k: v for k, v in item.items() if k != 'locator'} for item in options_list]
        path = Path("reports") / filename

        try:
            with path.open("w", encoding="utf-8") as f:
                json.dump(options_list_without_locator, f, indent=2)
            logger.info(f"Results written to {path}")

            with path.open("r", encoding="utf-8") as f:
                allure.attach(
                    f.read(),
                    name=filename,
                    attachment_type=allure.attachment_type.JSON
                )
            logger.info("Results successfully attached to Allure.")

        except Exception as e:
            logger.error(f"Failed to save or attach analysis results: {e}")
