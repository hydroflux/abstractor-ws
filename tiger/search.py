from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from selenium_utilities.locators import locate_element_by_id

from selenium_utilities.element_interaction import center_element, get_parent_element, is_active_class

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
    search_navigation = locate_element_by_id(browser, search_navigation_id, "search navigation", True)
    if is_active_class(search_navigation):
        return
    else:
        browser.execute_script(search_script)
        assert search_title


def open_search_tab(browser):
    search_tab = locate_element_by_id(browser, search_tab_id, "search tab", True)
    center_element(browser, search_tab)
    if is_active_class(get_parent_element(search_tab)):
        return
    else:
        search_tab.click()


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
