from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from settings.general_functions import javascript_script_execution, timeout

from leopard.leopard_variables import (disclaimer_active_class,
                                       disclaimer_button_id, disclaimer_id,
                                       search_script)


def locate_disclaimer(browser):
    try:
        disclaimer_present = EC.presence_of_element_located((By.ID, disclaimer_id))
        WebDriverWait(browser, timeout).until(disclaimer_present)
        disclaimer = browser.find_element_by_id(disclaimer_id)
        return disclaimer
    except TimeoutException:
        print("Browser timed out while trying to locate disclaimer while logging in, please review.")


def locate_disclaimer_button(browser):
    try:
        disclaimer_button_present = EC.element_to_be_clickable((By.ID, disclaimer_button_id))
        WebDriverWait(browser, timeout).until(disclaimer_button_present)
        disclaimer_button = browser.find_element_by_id(disclaimer_button_id)
        return disclaimer_button
    except TimeoutException:
        print("Browser timed out while trying to locate disclaimer button while logging in, please review.")


def handle_disclaimer(browser):
    javascript_script_execution(browser, search_script)
    disclaimer = locate_disclaimer(browser)
    if disclaimer.get_attribute('class') == disclaimer_active_class:
        disclaimer_button = locate_disclaimer_button(browser)
        disclaimer_button.click()