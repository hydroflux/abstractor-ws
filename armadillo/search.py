from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from settings.general_functions import assert_window_title, get_field_value, javascript_script_execution, timeout
from settings.file_management import document_type, document_value, extrapolate_document_value

from armadillo.armadillo_variables import document_search_url, document_search_title, document_search_field_id, execute_document_search_script


def open_document_search(browser, document):
    browser.get(document_search_url)
    if not assert_window_title(browser, document_search_title):
        print(f'Browser failed to open document search link for '
              f'{extrapolate_document_value(document)}, please review.')
        input()


# Matches crocodile locate_document_search_field
def locate_document_search_field(browser, document):
    try:
        document_search_field_present = EC.element_to_be_clickable((By.ID, document_search_field_id))
        WebDriverWait(browser, timeout).until(document_search_field_present)
        document_search_field = browser.find_element_by_id(document_search_field_id)
        return document_search_field
    except TimeoutException:
        print(f'Browser timed out trying to locate document field for '
              f'{extrapolate_document_value(document)}.')


# Matches crocodile clear_document_search_field
def clear_document_search_field(browser, document):
    while get_field_value(locate_document_search_field(browser, document)) != '':
        locate_document_search_field(browser, document).clear()


# Matches crocodile enter_document_number
def enter_document_number(browser, document):
    while get_field_value(locate_document_search_field(browser, document)) != document_value(document):
        locate_document_search_field(browser, document).send_keys(Keys.UP + document_value(document))


# Matches crocodile handle_document_search_field
def handle_document_search_field(browser, document):
    clear_document_search_field(browser, document)
    enter_document_number(browser, document)


def document_search(browser, document):
    open_document_search(browser, document)
    handle_document_search_field(browser, document)
    javascript_script_execution(browser, execute_document_search_script)


# Matches crocodile 'search'
def search(browser, document):
    if document_type(document) == 'document_number':
        document_search(browser, document)
    else:
        print(f'Unable to search {document_type(document)}, new search path needs to be developed.')
        print("Please press enter after reviewing the search parameters...")
        input()
