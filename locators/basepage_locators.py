
class BasePageLocators:
    # Search Bar fields
    AIRBNB_MAIN_SEARCH_BAR = "[data-testid='structured-search-input-field-query']"
    AIRBNB_MAIN_SEARCH_LOCATION_INPUT = "[data-testid='structured-search-input-field-query']"
    AIRBNB_MAIN_SEARCH_LOCATION_BUTTON = "button[data-testid='little-search-location'] div"
    AIRBNB_MAIN_SEARCH_DATE = "[data-testid='structured-search-input-field-flex-dates']"
    AIRBNB_MAIN_SEARCH_DATE_BUTTON = "[data-testid='little-search-anytime'] div"
    AIRBNB_MAIN_SEARCH_GUESTS = "[data-testid='structured-search-input-field-guests-button']"
    AIRBNB_MAIN_SEARCH_GUESTS_BUTTON = "[data-testid='little-search-guests'] div:first-of-type"
    AIRBNB_MAIN_SEARCH_GUESTS_ADULTS_INCREASE = "[data-testid='stepper-adults-increase-button']"
    AIRBNB_MAIN_SEARCH_GUESTS_CHILD_INCREASE = "[data-testid='stepper-children-increase-button']"
    AIRBNB_MAIN_SEARCH_BUTTON = "[data-testid='structured-search-input-search-button']"
    AIRBNB_DATE_BUTTON_BY_DATE = 'button[data-state--date-string="{}"]'
    AIRBNB_MAIN_SEARCH_CHECKIN_DATE = '[data-testid="structured-search-input-field-split-dates-0"]'

    # Guest options list
    GUESTS_ADULTS_INCREASE = "[data-testid='stepper-adults-increase-button']"
    GUESTS_CHILDREN_INCREASE = "[data-testid='stepper-children-increase-button']"
    GUESTS_INFANTS_INCREASE = "[data-testid='stepper-infants-increase-button']"
    GUESTS_PETS_INCREASE = "[data-testid='stepper-pets-increase-button']"

    # Guest mapping
    GUEST_TYPE_INCREASE_SELECTORS = {
        "adults": GUESTS_ADULTS_INCREASE,
        "children": GUESTS_CHILDREN_INCREASE,
        "infants": GUESTS_INFANTS_INCREASE,
        "pets": GUESTS_PETS_INCREASE
    }