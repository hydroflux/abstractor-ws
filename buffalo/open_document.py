from buffalo.validation import page_is_loaded
from buffalo.buffalo_variables import search_results_header_text


def open_document(browser):
    if page_is_loaded(browser, search_results_header_text):
        pass
