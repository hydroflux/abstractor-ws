from engines.buffalo.frame_handling import switch_to_main_frame

from selenium_utilities.inputs import enter_input_value
from selenium_utilities.locators import locate_element, locate_element_by_name
from selenium_utilities.open import assert_window_title, open_url

from settings.general_functions import javascript_script_execution


def enter_credentials(browser, abstract):
    enter_input_value(browser, locate_element_by_name, abstract.county.credentials[0],
                      "username input", abstract.county.credentials[1])
    enter_input_value(browser, locate_element_by_name, abstract.county.credentials[2],
                      "password input", abstract.county.credentials[3])


def execute_login(browser, abstract):
    javascript_script_execution(browser, abstract.county.scripts["Login"])
    assert_window_title(browser, abstract.county.titles["Login"])


def handle_disclaimer(browser, abstract):
    switch_to_main_frame(browser, abstract)
    javascript_script_execution(browser, abstract.county.scripts["Disclaimer"])


def verify_login(browser, abstract):
    switch_to_main_frame(browser, abstract)
    welcome_message = locate_element(browser, "id", abstract.county.ids["Welcome"], "welcome message")
    if welcome_message.text == abstract.county.messages["Welcome"]:
        print('\nLogin successful, continuing program execution.')
        return True


def execute_login_process(browser, abstract):
    open_url(browser, abstract.county.urls["Home Page"],
             abstract.county.titles["Home Page"], "county site")
    enter_credentials(browser, abstract)
    execute_login(browser, abstract)
    handle_disclaimer(browser, abstract)
    return verify_login(browser, abstract)


def login(browser, abstract):
    print("\nWebdriver initialized, attempting to login...")
    if not execute_login_process(browser, abstract):
        print("Browser failed to properly login, please review & try again later.")
        browser.quit()
        exit()
