from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from .variables import (clear_search_id, instrument_search_id, naptime,
                       search_button_id, search_title, search_url, timeout)


def open_search(browser):
    browser.get(search_url)
    assert search_title


def clear_search(browser):
    try:
        clear_search_present = EC.presence_of_element_located((By.ID, clear_search_id))
        WebDriverWait(browser, timeout).until(clear_search_present)
        clear_search = browser.find_element_by_id(clear_search_id)
        browser.execute_script("arguments[0].scrollIntoView();", clear_search)
        clear_search.click()
    except TimeoutException:
        print("Browser timed out while trying to clear the search form.")


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


def document_number_search(browser, document_number):
    open_search(browser)
    clear_search(browser)
    naptime()
    # browser.refresh()
    enter_document_number(browser, document_number)
    execute_search(browser)
