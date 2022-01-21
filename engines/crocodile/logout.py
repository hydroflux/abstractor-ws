from selenium_utilities.open import assert_window_title
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from settings.general_functions import timeout

from settings.county_variables.crocodile import logout_button_id, website_title


def locate_logout_button(browser):
    try:
        logout_button_present = EC.element_to_be_clickable((By.ID, logout_button_id))
        WebDriverWait(browser, timeout).until(logout_button_present)
        logout_button = browser.find_element_by_id(logout_button_id)
        return logout_button
    except TimeoutException:
        print("Browser timed out trying to locate logout button, please review.")


def execute_logout(browser):
    logout_button = locate_logout_button(browser)
    logout_button.click()


def verify_logout(browser):
    if not assert_window_title(browser, website_title):
        print('Unable to verify logout, please review.')


def logout(browser):
    execute_logout(browser)
    verify_logout(browser)
