import logging
import re

from pages.base_page import BasePage
from playwright.sync_api import Page
from locators.rooms_locators import RoomsLocators

class RoomPage(BasePage):
    """
    Page object representing the Room Details page of an Airbnb listing.
    Provides functionality to reserve the room and extract reservation summary details.
    """
    def __init__(self, page: Page):
        """
        Initializes the RoomPage object.

        Args:
            page (Page): The Playwright page instance for interacting with the browser context.
        """
        super().__init__(page)
        self.reservation_details_list = None

    def click_reserve_button(self):
        """
        Clicks the second 'Reserve' button on the room details page.
        """
        self.page.locator(RoomsLocators.RESERVE_BUTTON).nth(1).click()

    def reservation_details(self):
        """
                Extracts and parses reservation information from the confirmation section.

                The following details are collected:
                    - name: Name or title of the listing.
                    - price: Total reservation price.
                    - rating: Guest rating of the listing.
                    - date: Reservation date range.
                    - guest: Guest details (e.g., number of adults/children).

                This data is stored in the `self.reservation_details_list` attribute.

                Raises:
                    ValueError: If parsing of any required field fails.
                """
        details_list = []
        section_text = self.page.locator(RoomsLocators.CONFIRM_PAY_DETAILS).text_content()
        logging.info(f'Reservation Text are:\n{section_text}')
        name = section_text.split("Rating ")[0]
        rating = float(section_text.split("Rating ")[1].split(" out")[0])
        date = section_text.split("Trip details")[1].split(',')[0].replace("\u2009", " ").replace("\u2013", "–")
        guest = re.search(r'\d{4}\s*(.*)', section_text.split("details")[1].split("Change")[0]).group(1).strip()
        price = float(re.search(r'Total[^0-9]*([\d.,]+)', section_text).group(1).replace(',', ''))

        details_list.append({
            'name': name,
            'price': price,
            'rating': rating,
            'date': date,
            'guest': guest
        })

        logging.info(f'The reservation details list are:\n{details_list}')
        self.reservation_details_list =  details_list
