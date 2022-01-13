from selenium_utilities.open import open_url

from settings.county_variables.jaguar import search_url, search_title


def clear_search(browser, document):
    pass


def handle_document_value_numbers(browser, document):
    pass


def execute_search(browser, document):
    pass


def search(browser, document):
    open_url(browser, search_url, search_title, "document search page")
    clear_search(browser, document)
