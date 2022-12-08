from settings.general_functions import javascript_script_execution
from selenium_utilities.open import assert_window_title

from engines.buffalo.frame_handling import switch_to_default_content


def log_out_user(browser, abstract):
    switch_to_default_content(browser)
    javascript_script_execution(browser, abstract.county.scripts["Logout"])


def verify_logout(browser, abstract):
    if not assert_window_title(browser, abstract.county.titles["Home Page"]):
        print('Browser failed to successfully log out user, please review.')
        input()
    else:
        return True


def logout(browser, abstract):
    log_out_user(browser, abstract)
    if verify_logout(browser, abstract):
        browser.quit()
        exit()
