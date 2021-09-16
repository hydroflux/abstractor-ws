from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from settings.general_functions import (get_direct_link,
                                        javascript_script_execution,
                                        set_description_link, timeout)

from rattlesnake.rattlesnake_variables import (result_link_tag,
                                               result_row_tag_name,
                                               results_table_id)
from rattlesnake.validation import validate_result_reception_number, validate_result_volume_and_page_numbers


def locate_search_results(browser, document):
    try:
        search_results_present = EC.presence_of_element_located((By.ID, results_table_id))
        WebDriverWait(browser, timeout).until(search_results_present)
        search_results = browser.find_element_by_id(results_table_id)
        return search_results
    except TimeoutException:
        print(f'Browser timed out trying to locate search results for '
              f'{document.extrapolate_value()}, please review.')
        input()


def locate_search_result_rows(search_results, document):
    try:
        result_rows_present = EC.presence_of_element_located((By.TAG_NAME, result_row_tag_name))
        WebDriverWait(search_results, timeout).until(result_rows_present)
        result_rows = search_results.find_elements_by_tag_name(result_row_tag_name)
        return result_rows
    except TimeoutException:
        print(f'Browser timed out trying to locate search result rows for '
              f'{document.extrapolate_value()}, please review.')
        input()


# Search results can also be used to identify the number of results pages
def get_search_result_rows(browser, document):
    search_results = locate_search_results(browser, document)
    result_rows = locate_search_result_rows(search_results, document)
    return result_rows[1:-1]


def count_results(browser, document):
    result_rows = get_search_result_rows(browser, document)
    for _ in result_rows:
        document.number_results += 1


def get_result(browser, document, result_number=0):
    return get_search_result_rows(browser, document)[result_number]


def locate_result_link(result, document):
    try:
        result_link_present = EC.element_to_be_clickable((By.TAG_NAME, result_link_tag))
        WebDriverWait(result, timeout).until(result_link_present)
        result_link = result.find_element_by_tag_name(result_link_tag)
        return result_link
    except TimeoutException:
        print(f'Browser timed out trying to locate result link for '
              f'{document.extrapolate_value()}, please review.')
        input()


def get_result_link(result, document):
    result_link = locate_result_link(result, document)
    return get_direct_link(result_link)


def open_result_link(browser, document, result):
    try:
        document_link = get_result_link(result, document)
        set_description_link(document, document_link)
        javascript_script_execution(browser, document.description_link)
        return True
    except TimeoutException:
        print(f'Browser timed out trying to open result link for '
              f'{document.extrapolate_value()}, please review')
        input()
        return False


def handle_result_document_type(browser, result, document):
    if document.type == 'document_number' and validate_result_reception_number(result, document):
        return open_result_link(browser, document, result)
    elif document.type == 'volume_and_page' and validate_result_volume_and_page_numbers(result, document):
        return open_result_link(browser, document, result)
    else:
        print(f'Browser encountered issues validating document type '
              f'"{document.type}" for "{document.document_value()}", please review.')
        input()


def open_result(browser, document, result_number):
    result = get_result(browser, document, result_number)
    return handle_result_document_type(browser, result, document)


def handle_search_results(browser, document, result_number):
    if document.number_results == 0:
        return False
    else:
        return open_result(browser, document, result_number)


def open_document(browser, document, result_number=0):
    if result_number == 0:
        count_results(browser, document)
    return handle_search_results(browser, document, result_number)
