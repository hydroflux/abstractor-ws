from selenium.common.exceptions import ElementClickInterceptedException

from project_management.timers import naptime
from selenium_utilities.locators import locate_element
from settings.general_functions import scroll_to_top

from engines.buffalo.frame_handling import switch_to_document_frame


def get_next_result_button(browser, abstract, document):
    switch_to_document_frame(browser, abstract)
    return locate_element(browser, "id", abstract.county.buttons["Next Result"],
                          "next result button", True, document)


def click_result_button(browser, button):
    try:
        scroll_to_top(browser)
        button.click()
        # short_nap()  # Nap is necessary, consider lengthening if app breaks at this point
        return True
    except ElementClickInterceptedException:
        print("Button click intercepted while trying to view previous / next result, trying again")


def handle_click_next_result_button(browser, abstract, document, button):
    while not click_result_button(browser, button):
        naptime()
        button = get_next_result_button(browser, abstract, document)


def next_result(browser, abstract, document):
    next_result_button = get_next_result_button(browser, abstract, document)
    handle_click_next_result_button(browser, abstract, document, next_result_button)
