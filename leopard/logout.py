from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from leopard.leopard_variables import logout_button_id
from settings.general_functions import timeout

# Use the following print statement to identify the best way to manage imports for Django vs the script folder
print("logout", __name__)


def locate_logout_button(browser):
    try:
        logout_button_present = EC.presence_of_element_located((By.ID, logout_button_id))
        WebDriverWait(browser, timeout).until(logout_button_present)
        logout_button = browser.find_element_by_id(logout_button_id)
        return logout_button
    except TimeoutException:
        print("Browser timed out while trying to locate logout button, please review.")


def get_logout_link(browser):
    logout_button = locate_logout_button(browser)
    return logout_button.get_attribute("href")


def logout(browser):
    logout_link = get_logout_link(browser)
    browser.get(logout_link)
