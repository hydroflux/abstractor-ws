from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from buffalo.frame_handling import switch_to_search_result_list_frame
from settings.file_management import document_type, extrapolate_document_value
from settings.general_functions import timeout

from buffalo.validation import page_is_loaded
from buffalo.buffalo_variables import search_results_header_text, first_result_id


def locate_first_result(browser, document):
    try:
        first_result_present = EC.element_to_be_clickable((By.ID, first_result_id))
        WebDriverWait(browser, timeout).until(first_result_present)
        first_result = browser.find_element_by_id(first_result_id)
        return first_result
    except TimeoutException:
        print(f'Browser timed out trying to locate first search result for '
              f'{extrapolate_document_value(document)}, please review.')


def verify_first_result(browser, document):
    switch_to_search_result_list_frame(browser)
    first_result = locate_first_result(browser, document)


def open_document_number(browser, document):
    pass


def process_open_document(browser, document):
    if document_type(document) == "document_number":
        open_document_number(browser, document)
    else:
        print(f'Document type {document_type(document)} not currently available, '
              f'please review entry...')
        input()


def open_document(browser, document):
    if page_is_loaded(browser, search_results_header_text):
        process_open_document(browser, document)
