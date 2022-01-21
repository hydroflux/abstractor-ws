from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from settings.county_variables.buffalo import (first_result_id,
                                               search_results_header_text)
from settings.file_management import (document_type, document_value,
                                      extrapolate_document_value)
from settings.general_functions import eight_character_padding, timeout

from engines.buffalo.frame_handling import switch_to_search_result_list_frame
from engines.buffalo.validation import page_is_loaded


def locate_first_result(browser, document):
    try:
        first_result_present = EC.element_to_be_clickable((By.ID, first_result_id))
        WebDriverWait(browser, timeout).until(first_result_present)
        first_result = browser.find_element_by_id(first_result_id)
        return first_result
    except TimeoutException:
        print(f'Browser timed out trying to locate first search result for '
              f'{extrapolate_document_value(document)}, please review.')
        input()


def get_first_result(browser, document):
    switch_to_search_result_list_frame(browser)
    return locate_first_result(browser, document)


def verify_first_document_search_result(browser, document):
    first_result = get_first_result(browser, document).text
    if first_result == eight_character_padding(document_value(document)):
        return True


def open_document_number(browser, document):
    if verify_first_document_search_result(browser, document):
        get_first_result(browser, document).click()
    else:
        print(f'First search result located does not match the searched document '
              f'{extrapolate_document_value(document)}, please review')
        input()


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
        return True
