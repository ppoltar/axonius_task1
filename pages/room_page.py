import re

from pages.base_page import BasePage
from playwright.sync_api import Page
from locators.rooms_locators import RoomsLocators


class RoomPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

    def click_reserve_button(self):
        self.page.locator(RoomsLocators.RESERVE_BUTTON).nth(1).click()

    def attempt_reservation(self):
        # Locate the element by data-testid
        section_text = self.page.locator('[data-section-id="PRODUCT_DETAILS"]').text_content()

        name = section_text.split("Rating ")[0]
        rating = float(section_text.split("Rating ")[1].split(" out")[0])
        date = section_text.split("Trip details")[1].split(',')[0]

        price_string = section_text.split("Price breakdown")[0].split("Total ")[1]
        match = re.search(r'([\d.,]+)', price_string)
        price = float(match.group(1).replace(',', ''))




        pass