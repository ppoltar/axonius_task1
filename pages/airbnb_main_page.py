import logging
from playwright.sync_api import Page
from locators.airbnb_locators import AirbnbLocators
from locators.basepage_locators import BasePageLocators
from locators.rooms_locators import RoomsLocators
from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class AirbnbMainPage(BasePage):
    """
    AirbnbMainPage is a page object model that encapsulates interactions with Airbnb's main page.
    """

    def __init__(self, page: Page):
        """
        Initializes the AirbnbMainPage with a Playwright page instance.

        Args:
            page (playwright.sync_api.Page): The Playwright page object used for browser interaction.
        """
        super().__init__(page)
        self.place_options = None

    def go_to_airbnb_main_page(self):
        """
        Navigates to the Airbnb main page and waits for the search bar to be visible.

        Raises:
            Exception: If navigation to the Airbnb page fails or if the search bar is not visible within the timeout period.
        """
        try:
            self.page.goto(AirbnbLocators.AIRBNB_URL)
            self.page.locator(BasePageLocators.AIRBNB_MAIN_SEARCH_BAR).wait_for(state="visible")
        except Exception as e:
            error_message = f"Failed to go to the page: {AirbnbLocators.AIRBNB_URL}. Error: {str(e)}"
            logger.error(error_message)
            raise Exception(f"Page navigation failed: {error_message}")

    def place_options_results_sorted_by_rating_price(self, wanted_dates: str):
        """
        Extracts, filters, and sorts the list of place options based on their rating and price.

        Args:
            wanted_dates (str): The dates to match in the URL of the listings.

        Raises:
            Exception: If there is an error in parsing the listing's details such as price, rating, or URL.
        """
        self.page.locator(AirbnbLocators.CARD_CONTAINER).nth(0).wait_for(state="visible")
        options = self.page.locator(AirbnbLocators.CARD_CONTAINER).all()

        options_list = []
        for option in options:
            try:
                link_locator = option.locator(AirbnbLocators.CARD_ROOM_URL).first
                href_link = link_locator.get_attribute("href")
                if not wanted_dates in href_link:
                    continue
            except Exception as e:
                logger.warning(f"Error while parsing listing dates or URL: {e}")
                continue

            name_locator = option.locator(AirbnbLocators.CARD_NAME)
            name = name_locator.text_content() if name_locator else "No name"

            price_locator = option.locator(AirbnbLocators.CARD_PRICE)
            price_text = price_locator.text_content() if price_locator else ""
            try:
                price = float(price_text.split(" total")[0].split("₪")[-1].replace(',', '')) if price_text else 0.0
            except ValueError:
                price = 0.0  # Fallback in case price conversion fails

            # Extract rating
            try:
                rating_locator = (option.locator(AirbnbLocators.CARD_RATING_SPAN).
                                  filter(has_text=AirbnbLocators.CARD_RATING_TEXT).nth(0))
                rating_text = rating_locator.text_content() if rating_locator else "0"
                rating = float(rating_text.split(" ")[0])  # Extract rating number before 'out of 5'
            except Exception as e:
                # Log error if the rating isn't found or there's an issue
                logger.warning(f'Cannot find rating for: {name} due to error: {str(e)}')
                rating = 0.0  # Default rating if not found

            options_list.append({
                'name': name,
                'price': price,
                'rating': rating,
                'locator': option
            })

        self.place_options = sorted(options_list, key=lambda x: (-x['rating'], x['price']))

    def most_rating_and_cheapest_option(self):
        """
        Returns the most highly-rated and cheapest option from the list of available places.

        Returns:
            dict: The dictionary containing details of the most rated and cheapest place.
        """
        return self.place_options[0]

    def choose_most_rating_and_cheapest_option(self):
        """
        Clicks on the most highly-rated and cheapest place option. Handles popups if they appear.

        Raises:
            Exception: If selecting the most highly-rated and cheapest option fails, or if there is an issue handling the popup.
        """
        try:
            logger.info("Clicking on the most rated and cheapest option...")
            with self.page.context.expect_page() as popup_info:
                self.most_rating_and_cheapest_option()["locator"].click()

            popup_page = popup_info.value
            popup_page.wait_for_load_state()

            try:
                popup = popup_page.locator(RoomsLocators.TRANSLATION_POPUP_X)
                popup.wait_for(state="visible")
                popup.click()
                logger.info("Popup appeared and was clicked.")
            except Exception as e:
                logger.warning(f"Popup did not appear, proceeding to the next step. : {e}")

            return popup_page

        except Exception as e:
            logger.error(f"Failed choose place option: {e}")
            raise Exception(f"Failed to select the most rated and cheapest option: {e}")

    def click_on_filter(self):
        """
        Clicks on the filter button to open the filter menu for further customization of search results.
        """
        self.page.locator(AirbnbLocators.AIRBNB_MAIN_FILTER_BUTTON).click()

    def click_instant_book(self):
        """
        Selects the 'Instant Book' filter to show only instant-bookable places.
        """
        self.page.locator(AirbnbLocators.FILTER_INSTANT_BOOK).click()

    def click_filter_show_footer(self):
        """
        Clicks on the 'Show footer' filter to toggle the footer visibility in the filter section.
        """
        self.page.locator(AirbnbLocators.FILTER_SHOW_FOOTER).click()

    def click_filter_entire_home(self):
        """
        Selects the 'Entire home' filter to show only entire properties for rent.
        """
        self.page.locator(AirbnbLocators.FILTER_ENTIRE_HOME).click()
