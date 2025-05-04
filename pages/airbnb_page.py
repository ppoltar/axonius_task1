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

    def click_checkin_date(self):
        self.page.locator(AirbnbLocators.AIRBNB_MAIN_SEARCH_CHECKIN_DATE).click()

    def select_date_in_search_bar(self, date: str):
        selector = AirbnbLocators.AIRBNB_DATE_BUTTON_BY_DATE.format(date)
        self.page.click(selector)

    def choose_checkin_checkout_date(self, checkin_date: str, checkout_date: str):
        self.click_checkin_date()
        self.select_date_in_search_bar(checkin_date)
        self.select_date_in_search_bar(checkout_date)

    def click_search_button_in_search_bar(self):
        self.page.locator(AirbnbLocators.AIRBNB_MAIN_SEARCH_BUTTON).click()

    def location_button(self):
        return self.page.locator(AirbnbLocators.AIRBNB_MAIN_SEARCH_LOCATION_BUTTON)

    def date_button(self):
        return self.page.locator(AirbnbLocators.AIRBNB_MAIN_SEARCH_DATE_BUTTON)

    def guests_button(self):
        return self.page.locator(AirbnbLocators.AIRBNB_MAIN_SEARCH_GUESTS_BUTTON)

    def options_results_sorted_by_rating_price(self):
        options =  self.page.locator("[data-testid='card-container']").all()

        options_list = []
        for option in options:
            name_locator = option.locator('[data-testid="listing-card-name"]')
            name = name_locator.text_content() if name_locator else "No name"

            price_locator = option.locator('[data-testid="price-availability-row"]')
            price_text = price_locator.text_content() if price_locator else ""
            try:
                price = float(price_text.split(" total")[0].split("₪")[-1].replace(',', '')) if price_text else 0.0
            except ValueError:
                price = 0.0  # Fallback in case price conversion fails

            # Extract rating
            try:
                rating_locator = option.locator("span").filter(has_text="out of 5 average rating").nth(0)
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

        return sorted(options_list, key=lambda x: (-x['rating'], x['price']))


