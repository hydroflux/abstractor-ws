from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from settings.general_functions import timeout

from rattlesnake.logout import verify_logout
from rattlesnake.rattlesnake_variables import logout_button_id


def locate_logout_button(browser):
    try:
        logout_button_present = EC.element_to_be_clickable((By.ID, logout_button_id))
        WebDriverWait(browser, timeout).until(logout_button_present)
        logout_button = browser.find_element_by_id(logout_button_id)
        return logout_button
    except TimeoutException:
        print("Browser timed out while trying to locate logout button, please review.")


def execute_logout(browser):
    logout_button = locate_logout_button(browser)
    logout_button.click()


def logout(browser):
    execute_logout(browser)
    verify_logout(browser)
