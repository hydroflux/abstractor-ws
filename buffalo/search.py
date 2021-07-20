from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from settings.file_management import document_type


def open_search(browser, document):
    pass


def open_document_search_menu(browser, document):
    pass


def clear_document_search_field(browser, document):
    pass


def enter_document_number(browser, document):
    pass


def handle_document_search_field(browser, document):
    enter_document_number(browser, document)
    clear_document_search_field(browser, document)


def execute_search(browser, document):
    pass


def document_search(browser, document):
    handle_document_search_field(browser, document)
    execute_search(browser, document)


def search(browser, document):
    if document_type(document) == "document_number":
        document_search(browser, document)
    else:
        print(f'Unable to search {document_type(document)}, new search path needs to be developed.')
        print("Please press enter after reviewing the search parameters...")
        input()
