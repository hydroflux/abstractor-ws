from selenium.webdriver.common.keys import Keys

from selenium_utilities.search import locate_search_field_by_id as locate_search_field

from settings.file_management import document_value
from settings.general_functions import (get_field_value,
                                        javascript_script_execution)

from armadillo.armadillo_variables import (document_search_url,
                                           execute_document_search_script)
from armadillo.validation import verify_document_search_page_loaded


def open_document_search(browser):
    browser.get(document_search_url)


def clear_search_field(browser, document, type, id):
    while get_field_value(locate_search_field(browser, document, id, type)) != '':
        locate_search_field(browser, document, id, type).clear()


def clear_search(browser, document):
    clear_search_field(browser, document, "reception number", document.search_field_ids["Reception Number"])
    clear_search_field(browser, document, "volume", document.search_field_ids["Volume"])
    clear_search_field(browser, document, "page", document.search_field_ids["Page"])


def execute_search(browser):
    javascript_script_execution(browser, execute_document_search_script)


def enter_value_number(browser, document, type, id, value):
    while get_field_value(locate_search_field(browser, document, id, type)) != value:
        locate_search_field(browser, document, id, type).send_keys(Keys.UP + value)


def handle_document_value_numbers(browser, document):
    value = document_value(document)
    if document.type == 'document_number':
        enter_value_number(browser, document, document.type, document.search_field_ids["Reception Number"], value)
    elif document.type == 'volume_and_page':
        enter_value_number(browser, document, document.type, document.search_field_ids["Volume"], value[0])
        enter_value_number(browser, document, document.type, document.search_field_ids["Page"], value[1])
    else:
        print(f'Unable to search document type "{document.type}", '
              f'a new search path needs to be developed in order to continue.\n')
        print("Please press enter after reviewing the search parameters...")
        input()


def document_search(browser, document):
    handle_document_value_numbers(browser, document)
    execute_search(browser)


def search(browser, document):
    open_document_search(browser)
    verify_document_search_page_loaded(browser, document)
    clear_search(browser, document)
    document_search(browser, document)
