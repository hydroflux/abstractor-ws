from selenium.common.exceptions import (StaleElementReferenceException,
                                        TimeoutException)

from project_management.timers import micro_nap

from selenium_utilities.inputs import click_button, enter_input_value
from selenium_utilities.locators import (locate_element_by_class_name,
                                         locate_element_by_id)
from selenium_utilities.open import open_url

from settings.county_variables.eagle import (credentials, fallback_search_url,
                                             home_page_title, home_page_url,
                                             logged_out_redirect_url,
                                             login_button_id,
                                             login_prompt_class)

from engines.eagle.disclaimer import check_for_disclaimer

# Use the following print statement to identify the best way to manage imports for Django vs the script folder
print("login", __name__)


def open_site(browser):
    open_url(browser, home_page_url, home_page_title, "county site")
    input("Press enter to login...")


def enter_credentials(browser):
    enter_input_value(browser, locate_element_by_id, credentials[0], "username input", credentials[1])
    enter_input_value(browser, locate_element_by_id, credentials[2], "password input", credentials[3])
    click_button(browser, locate_element_by_id, login_button_id, "login button")


def read_login_message(browser):
    try:
        login_message = locate_element_by_id(browser, credentials[5], "login message", True)
        return login_message.text
    except StaleElementReferenceException:
        print('Encountered StaleElementReferenceException '
              'attempting to read login message, trying again.')


def confirm_login(browser):
    while read_login_message(browser) != credentials[4]:
        micro_nap()


def log_back_in(browser):
    try:
        click_button(browser, locate_element_by_class_name,
                     login_prompt_class, login_button_id, "login button prompt")
        enter_credentials(browser)
        confirm_login(browser)
    except TimeoutException:
        print("Browser timed out while trying to log back in after logout.")


def check_login_status(browser):
    while browser.current_url == logged_out_redirect_url:
        print('Browser redirected to login screen, checking login status & returning to search.')
        if read_login_message(browser) != credentials[4]:
            print('Browser logged out, attempting to log back in.')
            log_back_in(browser)
        browser.get(fallback_search_url)


def execute_login_process(browser):
    open_site(browser)
    check_for_disclaimer(browser)
    click_button(browser, locate_element_by_class_name,
                 login_prompt_class, login_button_id, "login button prompt")
    enter_credentials(browser)
    confirm_login(browser)
    return True


def login(browser):
    print("\nWebdriver initialized, attempting to login...")
    if not execute_login_process(browser):
        print("Login sequence failed, attempting again before closing out.")
        if not execute_login_process(browser):
            print("Browser failed to properly login, please review & try again later.")
            browser.quit()
            exit()
