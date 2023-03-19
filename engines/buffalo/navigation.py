from selenium.common.exceptions import ElementClickInterceptedException

from project_management.timers import naptime
from selenium_utilities.locators import locate_element

from engines.buffalo.frame_handling import switch_to_main_frame, switch_to_document_frame


def get_next_result_button(browser, abstract, document):
    switch_to_document_frame(browser, abstract)
    return locate_element(browser, "id", abstract.county.buttons["Next Result"],
                          "next result button", True, document)


def clear_download_alert(browser, abstract, document):
    switch_to_main_frame(browser, abstract)
    clear_download_alert_button = locate_element(browser, "class", abstract.county.buttons["Download Alert"],
                                                 "download alert button", True, document, True)
    clear_download_alert_button.click()


def execute_next_result_click(browser, abstract, document):
    try:
        next_result_button = get_next_result_button(browser, abstract, document)
        # handle_click_next_result_button(browser, abstract, document, next_result_button)
        next_result_button.click()
        return True
    except ElementClickInterceptedException:
        print("Encountered an ElementClickInterceptedException, trying again...")
        clear_download_alert(browser, abstract, document)
        return False


def next_result(browser, abstract, document):
    while not execute_next_result_click(browser, abstract, document):
        # Add an alert text fix if naptime does not fix issue
        naptime()
        # added 03/20/23
        execute_next_result_click(browser, abstract, document)
