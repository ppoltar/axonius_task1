import allure
import pytest
import logging

from pages.room_page import RoomPage
from tests.e2e_data import e2e_test_data
from pages.airbnb_main_page import AirbnbMainPage
from playwright.sync_api import expect

logger = logging.getLogger(__name__)

@allure.description("""
This test verifies the end-to-end flow of searching for a location, selecting dates and guests, 
    applying filters, validating the search parameters, and confirming the reservation details on Airbnb.

    Test Steps:
    1. Navigate to the Airbnb main page.
    2. Choose a location, check-in/check-out dates, and number of guests in the search bar.
    3. Apply filters to search results (such as selecting 'Entire Home' and 'Instant Book').
    4. Validate the URL contains the expected search parameters (location, dates, guests).
    5. Validate the UI displays the correct search parameters.
    6. Sort search results by rating and price.
    7. Select the most highly-rated and cheapest option.
    8. Go to the room page and reserve the selected apartment.
    9. Validate reservation details such as name, price, rating, guest count, and reservation date.

    Expected Results:
    - The search parameters should reflect the location, dates, and guests.
    - The filters should correctly narrow the search to relevant results.
    - The reservation details on the room page should match the selected property and the search parameters.
""")

@pytest.mark.e2e
@pytest.mark.parametrize("test_data", e2e_test_data, ids=[data["case"] for data in e2e_test_data])
def test_e2e(page, test_data):
    """
    End-to-End test for the Airbnb reservation flow. This simulates a user flow for searching properties,
    applying filters, and reserving a property while validating the correctness of the results.

    Args:
        page (Page): The Playwright page object.
        test_data (dict): A dictionary containing test case parameters, such as location, check-in,
                          check-out dates, expected reservation details, etc.
      Raises:
        Exception: If any validation step fails (e.g., mismatch in property name, price, or guest details).
    """
    logger.info(f"Starting test: {test_data['case']}.")
    airbnb_page = AirbnbMainPage(page)
    airbnb_page.go_to_airbnb_main_page()

    logger.info("Part-1  Choosing location, dates and guest.")
    airbnb_page.choose_where_in_search_bar(test_data['location'])
    airbnb_page.choose_checkin_checkout_date(test_data['checkin'], test_data['checkout'])
    airbnb_page.choose_who_in_search_bar(test_data['who'])
    airbnb_page.click_search_button_in_search_bar()
    logger.info("Finish Part-1. Good Job")

    logger.info("Part-2 Filters by entire place and instant book.")
    airbnb_page.click_on_filter()
    airbnb_page.click_filter_entire_home()
    airbnb_page.click_instant_book()
    airbnb_page.click_filter_show_footer()
    logger.info("Finish Part-2. Good Job")

    logger.info("Part-3 Validate search params by url.")
    expect(airbnb_page.page).to_have_url(test_data["expected_url"])
    logger.info("Finish Part-3. Good Job")

    logger.info("Part-4 Validate search params by ui.")
    expect(airbnb_page.location_button()).to_have_text(test_data['location'])
    expect(airbnb_page.date_button()).to_have_text(test_data['expected_dates'])
    expect(airbnb_page.guests_button()).to_have_text(test_data['expected_guest'])
    logger.info("Finish Part-4. Good Job")

    logger.info('Part-5 Find places sorted option by rating and price')
    airbnb_page.place_options_results_sorted_by_rating_price(test_data["checkin_checkout_query"])
    airbnb_page.save_attach_results(airbnb_page.place_options, filename="Analyze_Results.json")
    airbnb_page_tab = airbnb_page.choose_most_rating_and_cheapest_option()
    logger.info("Finish Part-5. Good Job")

    logger.info('Part-6 Find places sorted option by rating and price')
    room_page = RoomPage(airbnb_page_tab)
    room_page.click_reserve_button()
    logger.info("Finish Part-6. Good Job")

    logger.info('Part-7 Collect reservation and save the results')
    room_page.reservation_details()
    room_page.save_attach_results(room_page.reservation_details_list, filename="Reservation.json")
    logger.info("Finish Part-7. Good Job")

    logger.info('Part-8 Validate reservation')
    if not room_page.reservation_details_list[0]['name'] == airbnb_page.place_options[0]["name"]:
        raise Exception(f"The name of the apartment different: "
                        f"{room_page.reservation_details_list[0]['name']} != {airbnb_page.place_options[0]['name']}")

    if abs(round(room_page.reservation_details_list[0]["price"], 0) - round(airbnb_page.place_options[0]["price"], 0)) > test_data["price_ratio"] :
        raise Exception(f"The price of the apartment different in more than: {test_data['price_ratio']} "
                        f"{round(room_page.reservation_details_list[0]['price'], 0)} != {round(airbnb_page.place_options[0]['price'], 0)}")

    if not room_page.reservation_details_list[0]["rating"] == airbnb_page.place_options[0]["rating"]:
        raise Exception(f"The rating of the apartment different: "
                        f"{room_page.reservation_details_list[0]['rating']} != {airbnb_page.place_options[0]['rating']}")

    if not room_page.reservation_details_list[0]["guest"] == test_data["expected_reservation_guests"]:
        raise Exception(f"The guest of the apartment different: "
                        f"{test_data['expected_reservation_guests']} != {room_page.reservation_details_list[0]['guest']}")

    if not room_page.reservation_details_list[0]["date"].split() == test_data["expected_dates"].split():
        raise Exception(f"The date of the apartment reservation are different: "
                        f"{test_data['expected_dates']} != {room_page.reservation_details_list[0]['date']}")
    logger.info("Finish Part-8. Good Job")


