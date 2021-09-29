from selenium_utilities.inputs import (clear_input, click_button,
                                       enter_input_value)
from selenium_utilities.locators import locate_element_by_id as locate_input
from selenium_utilities.open import open_url

from settings.county_variables.eagle import search_title, search_url
from settings.general_functions import naptime

from eagle.login import check_login_status

# Use the following print statement to identify the best way to manage imports for Django vs the script folder
print("search", __name__)


# def get_clear_search_button(browser, document):
#     try:
#         clear_search_button_present = EC.presence_of_element_located((By.ID, clear_search_id))
#         WebDriverWait(browser, timeout).until(clear_search_button_present)
#         clear_search_button = browser.find_element_by_id(clear_search_id)
#         return clear_search_button
#     except TimeoutException:
#         print("Browser timed out trying to clear the search form.")
#         check_for_error(browser, document)


# def execute_clear_search(browser, button):
#     try:
#         center_element(browser, button)
#         button.click()
#         return True
#     except ElementClickInterceptedException:
#         print('Encountered an element click interception exception trying to clear the search form, '
#               'refreshing & trying again.')
#         return False
#     except JavascriptException:
#         print('Encountered an javascript exception trying to clear the search form, '
#               'refreshing & trying again.')
#         return False


# def clear_search(browser, document):
#     clear = False
#     while clear is not True:
#         clear_search_button = locate_element_by_id(browser, document.button_ids["Clear Search"],
#                                                    "clear search button", True, document)
#         clear = execute_clear_search(browser, clear_search_button)
#         if clear is False:
#             # browser.refresh()  #  Commented out on June 22, 2021
#             # medium_nap()  #  Commented out on June 22, 2021
#             browser.back()  # Should work for JS exceptions--don't know about Element Click Interceptions
#             medium_nap()
#             open_url(browser, search_url, search_title, "document search page")

def clear_search(browser, document):
    for id in document.input_ids:
        clear_input(browser, locate_input, document.input_ids[id], f'{id} Input', document)


# def handle_document_number_search_field(browser, document):
#     instrument_search_field = locate_input(browser, document.input_ids["Reception Number"],
#                                            "reception number input", True, document)
#     while type(instrument_search_field) is None:
#         check_for_error(browser, document)
#         instrument_search_field = locate_input(browser, document.input_ids["Reception Number"],
#                                                "reception number input", True, document)
#     return instrument_search_field


# def handle_book_search_field(browser, document):
#     book_search_field = locate_input(browser, document.input_ids["Book"],
#                                      "book input", True, document)
#     while type(book_search_field) is None:
#         check_for_error(browser, document)
#         book_search_field = locate_input(browser, document.input_ids["Book"],
#                                          "book input", True, document)
#     return book_search_field


# def handle_page_search_field(browser, document):
#     page_search_field = locate_input(browser, document.input_ids["Page"],
#                                      "page input", True, document)
#     while type(page_search_field) is None:
#         check_for_error(browser, document)
#         page_search_field = locate_input(browser, document.input_ids["Page"],
#                                          "page input", True, document)
#     return page_search_field


# Same as rattlesnake
def handle_document_value_numbers(browser, document):
    value = document.document_value()
    if document.type == "document_number":
        enter_input_value(browser, locate_input, document.input_ids["Reception Number"],
                          "reception number input", value, document)
        # If having issues, replace with the 'handle_xxx_search_field' functions
    elif document.type == "book_and_page":
        enter_input_value(browser, locate_input, document.input_ids["Book"],
                          "book input", value[0], document)
        enter_input_value(browser, locate_input, document.input_ids["Page"],
                          "page input", value[1], document)


def execute_search(browser, document):
    handle_document_value_numbers(browser, document)
    click_button(browser, locate_input, document.button_ids["Submit Search"],
                 "execute search button", document)


def search(browser, document):
    open_url(browser, search_url, search_title, "document search page")
    check_login_status(browser)
    clear_search(browser, document)
    naptime()  # Consider testing without this nap to see if necessary
    execute_search(browser, document)
