import logging
from playwright.sync_api import Page
from locators.airbnb_locators import AirbnbLocators
from locators.basepage_locators import BasePageLocators
from locators.rooms_locators import RoomsLocators
from pages.base_page import BasePage

logger = logging.getLogger(__name__)

class AirbnbMainPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.place_options = None


    def go_to_airbnb_main_page(self):
        """
        """
        try:
            self.page.goto(AirbnbLocators.AIRBNB_URL)
            self.page.locator(BasePageLocators.AIRBNB_MAIN_SEARCH_BAR).wait_for(state="visible")
        except Exception as e:
            error_message = f"Failed to go to the page: {AirbnbLocators.AIRBNB_URL}. Error: {str(e)}"
            logger.error(error_message)
            raise Exception(f"Page navigation failed: {error_message}")


    def place_options_results_sorted_by_rating_price(self):
        options =  self.page.locator(AirbnbLocators.CARD_CONTAINER).all()

        options_list = []
        for option in options:
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
                rating_locator =(option.locator(AirbnbLocators.CARD_RATING_SPAN).
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
        return self.place_options[0]

    def choose_most_rating_and_cheapest_option(self):
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
            except TimeoutError:
                logger.error("Popup did not appear, proceeding to the next step.")

            return popup_page

        except Exception as e:
            logger.error(f"Failed choose place option: {e}")

