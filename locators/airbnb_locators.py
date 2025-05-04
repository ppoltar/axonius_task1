
class AirbnbLocators:
    # Base URL
    AIRBNB_URL = "https://www.airbnb.com/"

    # Search Bar fields
    AIRBNB_MAIN_SEARCH_BAR = "[data-testid='structured-search-input-field-query']"
    AIRBNB_MAIN_SEARCH_LOCATION_INPUT = "[data-testid='structured-search-input-field-query']"
    AIRBNB_MAIN_SEARCH_DATE = "[data-testid='structured-search-input-field-flex-dates']"
    AIRBNB_MAIN_SEARCH_DATE_FLEXIBLE = "[data-testid='expanded-searchbar-dates-flexible-tab']"
    AIRBNB_MAIN_SEARCH_GUESTS = "[data-testid='structured-search-input-field-guests-button']"
    AIRBNB_MAIN_SEARCH_GUESTS_ADULTS_INCREASE = "[data-testid='stepper-adults-increase-button']"
    AIRBNB_MAIN_SEARCH_GUESTS_CHILD_INCREASE = "[data-testid='stepper-children-increase-button']"
    AIRBNB_MAIN_SEARCH_BUTTON = "[data-testid='structured-search-input-search-button']"

    # Guest steppers
    GUESTS_ADULTS_INCREASE = "[data-testid='stepper-adults-increase-button']"
    GUESTS_CHILDREN_INCREASE = "[data-testid='stepper-children-increase-button']"
    GUESTS_INFANTS_INCREASE = "[data-testid='stepper-infants-increase-button']"
    GUESTS_PETS_INCREASE = "[data-testid='stepper-pets-increase-button']"


    # Dynamic guest mapping for programmatic selection
    GUEST_TYPE_INCREASE_SELECTORS = {
        "adults": GUESTS_ADULTS_INCREASE,
        "children": GUESTS_CHILDREN_INCREASE,
        "infants": GUESTS_INFANTS_INCREASE,
        "pets": GUESTS_PETS_INCREASE
    }