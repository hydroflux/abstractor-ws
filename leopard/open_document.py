from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from settings.file_management import (document_type, document_value,
                                      extrapolate_document_value)
from settings.general_functions import (get_element_text, scroll_into_view,
                                        timeout)

from leopard.leopard_variables import (result_cell_tag, result_row_class,
                                       results_body_tag, results_count_id,
                                       results_id)

# Use the following print statement to identify the best way to manage imports for Django vs the script folder
print("open_document", __name__)

# Script is SIMILAR, but not nearly identical, to tiger open_document


def locate_result_count(browser, document):
    try:
        result_count_present = EC.presence_of_element_located((By.ID, results_count_id))
        WebDriverWait(browser, timeout).until(result_count_present)
        result_count = browser.find_element_by_id(results_count_id)
        return result_count
    except TimeoutException:
        print(f'Browser timed out trying to locate the number of results returned for '
              f'{extrapolate_document_value(document)}.')


def count_results(browser, document):
    result_count = locate_result_count(browser, document)
    return result_count.text.split(' ')[-1]


def get_results_table_body(browser, document):
    try:
        results_present = EC.presence_of_element_located((By.ID, results_id))
        WebDriverWait(browser, timeout).until(results_present)
        results = browser.find_element_by_id(results_id)
        scroll_into_view(browser, results)
        results_table_body = results.find_element_by_tag_name(results_body_tag)
        return results_table_body
    except TimeoutException:
        print(f'Browser timed out trying to get results table after searching '
              f'{extrapolate_document_value(document)}, please review.')


def get_all_results(browser, results_table_body, document):
    try:
        first_row_present = EC.presence_of_element_located((By.CLASS_NAME, result_row_class))
        WebDriverWait(browser, timeout).until(first_row_present)
        all_results = results_table_body.find_elements_by_class_name(result_row_class)
        return all_results
    except TimeoutException:
        print(f'Browser timed out while trying to get results for '
              f'{extrapolate_document_value(document)}, please review.')


def get_first_row(browser, results_table_body, document):
    all_results = get_all_results(browser, results_table_body, document)
    return all_results[0]


def identify_first_result(browser, document):
    results_table_body = get_results_table_body(browser, document)
    return get_first_row(browser, results_table_body, document)


def check_result(browser, document):
    first_result = identify_first_result(browser, document)
    first_result_cells = first_result.find_elements_by_tag_name(result_cell_tag)
    if document_type(document) == "document_number":
        if document_value(document) in map(get_element_text, first_result_cells):
            return True
    elif document_type(document) == "book_and_page":
        return True


def open_document(browser, document):
    count_results(browser, document)
    if check_result(browser, document):
        identify_first_result(browser, document).click()
        return True
