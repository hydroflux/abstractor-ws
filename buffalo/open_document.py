from settings.file_management import document_type
from buffalo.validation import page_is_loaded
from buffalo.buffalo_variables import search_results_header_text


def verify_document_number(browser, document):
    pass


def open_document_number(browser, document):
    pass


def process_open_document(browser, document):
    if document_type(document) == "document_number":
        open_document_number(browser, document)


def open_document(browser, document):
    if page_is_loaded(browser, search_results_header_text):
        process_open_document(browser, document)
