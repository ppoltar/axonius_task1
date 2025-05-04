import allure
import pytest
import logging

from pages.room_page import RoomPage
from tests.e2e_data import e2e_test_data
from pages.airbnb_main_page import AirbnbMainPage
from playwright.sync_api import expect

logger = logging.getLogger(__name__)

@allure.description("""
""")

@pytest.mark.e2e
@pytest.mark.parametrize("test_data", e2e_test_data, ids=[data["case"] for data in e2e_test_data])
def test_e2e(page, test_data):
    logger.info(f"Starting test: {test_data['case']}.")
    airbnb_page = AirbnbMainPage(page)
    airbnb_page.go_to_airbnb_main_page()

    logger.info(f"Choosing location, dates and guest.")
    airbnb_page.choose_where_in_search_bar(test_data['location'])
    airbnb_page.choose_checkin_checkout_date(test_data['checkin'], test_data['checkout'])
    airbnb_page.choose_who_in_search_bar(test_data['who'])
    airbnb_page.click_search_button_in_search_bar()


    logger.info(f"Validate search params by url.")
    expect(airbnb_page.page).to_have_url(test_data["expected_url"])

    logger.info(f"Validate search params by ui.")
    expect(airbnb_page.location_button()).to_have_text(test_data['location'])
    expect(airbnb_page.date_button()).to_have_text(test_data['expected_dates'])
    expect(airbnb_page.guests_button()).to_have_text(test_data['expected_guest'])

    logger.info(f'Find places sorted option by rating and price')
    airbnb_page.place_options_results_sorted_by_rating_price()
    airbnb_page.save_attach_results(airbnb_page.place_options, filename="Analyze_Results.json")
    airbnb_page_tab = airbnb_page.choose_most_rating_and_cheapest_option()

    room_page = RoomPage(airbnb_page_tab)
    room_page.click_reserve_button()

    room_page.reservation_details()
    room_page.save_attach_results(room_page.reservation_details_list, filename="Reservation.json")

    if not room_page.reservation_details_list[0]['name'] == airbnb_page.place_options[0]["name"]:
        raise Exception(f"The name of the apartment different: "
                        f"{room_page.reservation_details_list[0]['name']} != {airbnb_page.place_options[0]['name']}")

    if not int(room_page.reservation_details_list[0]["price"]) == int(airbnb_page.place_options[0]["price"]):
        raise Exception(f"The price of the apartment different: "
                        f"{int(room_page.reservation_details_list[0]['price'])} != {int(airbnb_page.place_options[0]['price'])}")

    if not room_page.reservation_details_list[0]["rating"] == airbnb_page.place_options[0]["rating"]:
        raise Exception(f"The rating of the apartment different: "
                        f"{room_page.reservation_details_list[0]['rating']} != {airbnb_page.place_options[0]['rating']}")

    if not room_page.reservation_details_list[0]["guest"] == test_data["expected_reservation_guests"]:
        raise Exception(f"The guest of the apartment different: "
                        f"{test_data['expected_reservation_guests']} != {room_page.reservation_details_list[0]['guest']}")

    if not room_page.reservation_details_list[0]["date"].split() == test_data["expected_dates"].split():
        raise Exception(f"The date of the apartment different: "
                        f"{test_data['expected_dates']} != {room_page.reservation_details_list[0]['date']}")




