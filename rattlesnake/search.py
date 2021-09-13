from rattlesnake.validation import verify_document_search_page_loaded
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from settings.file_management import (document_type, document_value,
                                      extrapolate_document_value)
from settings.general_functions import (assert_window_title, get_field_value,
                                        javascript_script_execution, timeout)

from armadillo.armadillo_variables import (document_search_field_id,
                                           document_search_title,
                                           document_search_url,
                                           execute_document_search_script)


# This needs to be a loop in order to check against the server error
def open_document_search(browser, document):
    browser.get(document_search_url)
    verify_document_search_page_loaded(browser, document)


# Matches matches crocodile & armadillo locate_document_search_field
def locate_document_search_field(browser, document):
    try:
        document_search_field_present = EC.element_to_be_clickable((By.ID, document_search_field_id))
        WebDriverWait(browser, timeout).until(document_search_field_present)
        document_search_field = browser.find_element_by_id(document_search_field_id)
        return document_search_field
    except TimeoutException:
        print(f'Browser timed out trying to locate document field for '
              f'{extrapolate_document_value(document)}.')


# Matches crocodile & armadillo clear_document_search_field
def clear_document_search_field(browser, document):
    while get_field_value(locate_document_search_field(browser, document)) != '':
        locate_document_search_field(browser, document).clear()


# Matches crocodile & armadillo enter_document_number
def enter_document_number(browser, document):
    while get_field_value(locate_document_search_field(browser, document)) != document_value(document):
        locate_document_search_field(browser, document).send_keys(Keys.UP + document_value(document))


def handle_document_search_field(browser, document):
    clear_document_search_field(browser, document)
    enter_document_number(browser, document)


def execute_search():
    pass


def document_search(browser, document):
    handle_document_search_field(browser, document)


# Matches armadillo 'search'
def search(browser, document):
    open_document_search(browser, document)
    if document_type(document) == 'document_number':
        document_search(browser, document)
    else:
        print(f'Unable to search document type "{document_type(document)}", '
              f'a new search path needs to be developed in order to continue.\n')
        print("Please press enter after reviewing the search parameters...")
        input()
