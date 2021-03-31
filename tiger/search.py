from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from .variables import search_script, search_title, timeout, instrument_search_id, search_button_id


def open_search(browser):
    browser.execute_script(search_script)
    assert search_title


def enter_document_number(browser, document_number):
    try:
        instrument_search_field_present = EC.presence_of_element_located((By.ID, instrument_search_id))
        WebDriverWait(browser, timeout).until(instrument_search_field_present)
        instrument_search_field = browser.find_element_by_id(instrument_search_id)
        instrument_search_field.clear()
        instrument_search_field.send_keys(document_number)
    except TimeoutException:
        print(f'Browser timed out while trying to fill document field for document number {document_number}.')


def execute_search(browser):
    try:
        search_button_present = EC.element_to_be_clickable((By.ID, search_button_id))
        WebDriverWait(browser, timeout).until(search_button_present)
        search_button = browser.find_element_by_id(search_button_id)
        search_button.click()
    except TimeoutException:
        print("Browser timed out while trying to execute search.")