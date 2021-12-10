from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from selenium_utilities.element_interaction import is_active_class

if __name__ == '__main__':
    from settings.county_variables.tiger import (instrument_search_id,
                                                 search_button_id,
                                                 search_navigation_id,
                                                 search_script, search_tab_id,
                                                 search_title)
    from settings.settings import timeout
else:
    from ..settings.county_variables.tiger import (instrument_search_id,
                                                   search_button_id,
                                                   search_navigation_id,
                                                   search_script,
                                                   search_tab_id, search_title)
    from ..settings.settings import timeout


def open_search(browser):
    try:
        search_navigation_present = EC.element_to_be_clickable((By.ID, search_navigation_id))
        WebDriverWait(browser, timeout).until(search_navigation_present)
        search_navigation = browser.find_element_by_id(search_navigation_id)
        if is_active_class(search_navigation):
            return
        browser.execute_script(search_script)
        assert search_title
    except TimeoutException:
        print("Browser timed out while trying to open the search navigation.")


def get_parent_element(element):
    # return element.find_element_by_xpath(".//ancestor::li")
    return element.find_element_by_xpath("..")


def open_search_tab(browser):
    try:
        search_tab_present = EC.element_to_be_clickable((By.ID, search_tab_id))
        WebDriverWait(browser, timeout).until(search_tab_present)
        search_tab = browser.find_element_by_id(search_tab_id)
        browser.execute_script("arguments[0].scrollIntoView();", search_tab)
        if is_active_class(get_parent_element(search_tab)):
            return
        search_tab.click()
    except TimeoutException:
        print("Browser timed out while trying to access the search tab.")


def enter_document_number(browser, document_number):
    try:
        instrument_search_field_present = EC.element_to_be_clickable((By.ID, instrument_search_id))
        WebDriverWait(browser, timeout).until(instrument_search_field_present)
        instrument_search_field = browser.find_element_by_id(instrument_search_id)
        instrument_search_field.clear()
        instrument_search_field.send_keys(document_number)
    except TimeoutException:
        print(f'Browser timed out while trying to fill document field for document number '
              f'{document_number}, trying again.')


def execute_search(browser):
    try:
        search_button_present = EC.element_to_be_clickable((By.ID, search_button_id))
        WebDriverWait(browser, timeout).until(search_button_present)
        search_button = browser.find_element_by_id(search_button_id)
        search_button.click()
    except TimeoutException:
        print("Browser timed out while trying to execute search.")


def search(browser, document_number):
    open_search(browser)
    open_search_tab(browser)
    enter_document_number(browser, document_number)
    execute_search(browser)
