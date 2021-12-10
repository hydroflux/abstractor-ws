from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium_utilities.inputs import click_button, enter_input_value
from selenium_utilities.locators import (locate_element_by_id,
                                         locate_element_by_name)
from selenium_utilities.open import open_url

if __name__ == '__main__':
    from settings.county_variables.tiger import (credentials,
                                                 handle_disclaimer_id,
                                                 login_button_name, website,
                                                 website_title)
    from settings.general_functions import timeout

    from tiger.search import open_search
else:
    from ..settings.county_variables.tiger import (credentials,
                                                   handle_disclaimer_id,
                                                   login_button_name, website,
                                                   website_title)
    from ..settings.general_functions import timeout
    from .search import open_search


def enter_credentials(browser):
    enter_input_value(browser, locate_element_by_id, credentials[0], "username input", credentials[1])
    enter_input_value(browser, locate_element_by_id, credentials[2], "password input", credentials[3])
    click_button(browser, locate_element_by_name, login_button_name, "login button")


def handle_disclaimer(browser):
    try:
        disclaimer_present = EC.element_to_be_clickable((By.ID, handle_disclaimer_id))
        WebDriverWait(browser, timeout).until(disclaimer_present)
        disclaimer = browser.find_element_by_id(handle_disclaimer_id)
        disclaimer.click()
    except TimeoutException:
        print("Browser timed out while trying to handle the website disclaimer.")


def account_login(browser):
    open_url(browser, website, website_title, "county site")
    enter_credentials(browser)
    open_search(browser)
    handle_disclaimer(browser)
