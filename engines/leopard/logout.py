from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from project_management.timers import timeout

# Use the following print statement to identify the best way to manage imports for Django vs the script folder
print("logout", __name__)


def locate_logout_button(browser, abstract):
    try:
        logout_button_present = EC.presence_of_element_located((By.ID, abstract.county.buttons["Logout"]))
        # Element to be clickable seems to make more sense, need to investigate the UI when
        # updating leopard again
        WebDriverWait(browser, timeout).until(logout_button_present)
        logout_button = browser.find_element_by_id(abstract.county.buttons["Logout"])
        return logout_button
    except TimeoutException:
        print("Browser timed out while trying to locate logout button, please review.")


def get_logout_link(browser, abstract):
    logout_button = locate_logout_button(browser, abstract)
    return logout_button.get_attribute("href")


def logout(browser, abstract):
    logout_link = get_logout_link(browser, abstract)
    browser.get(logout_link)
