from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from settings.file_management import (document_type, document_value,
                                      extrapolate_document_value,
                                      split_book_and_page)
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


def count_total_results(browser, document):
    result_count = locate_result_count(browser, document)
    #  If result count == none, perform a "re-search"
    return result_count.text.split(' ')[-1]


def locate_results_table(browser, document):
    try:
        results_present = EC.presence_of_element_located((By.ID, results_id))
        WebDriverWait(browser, timeout).until(results_present)
        results = browser.find_element_by_id(results_id)
        return results
    except TimeoutException:
        print(f'Browser timed out trying to locate results for '
              f'{extrapolate_document_value(document)}, please review.')


def locate_results_table_body(browser, document, results_table):
    try:
        results_table_body_present = EC.presence_of_element_located((By.TAG_NAME, results_body_tag))
        WebDriverWait(browser, timeout).until(results_table_body_present)
        results_table_body = results_table.find_element_by_tag_name(results_body_tag)
        return results_table_body
    except TimeoutException:
        print(f'Browser timed out trying to extrapolate the results table for '
              f'{extrapolate_document_value(document)}, please review.')


def get_results_table_body(browser, document):
    results = locate_results_table(browser, document)
    scroll_into_view(browser, results)
    return locate_results_table_body(browser, document, results)


def locate_result_rows(browser, document, results_table_body):
    try:
        first_row_present = EC.presence_of_element_located((By.CLASS_NAME, result_row_class))
        WebDriverWait(browser, timeout).until(first_row_present)
        result_rows = results_table_body.find_elements_by_class_name(result_row_class)
        return result_rows
    except TimeoutException:
        print(f'Browser timed out while trying to get result rows for '
              f'{extrapolate_document_value(document)}, please review.')


def get_result_rows(browser, document):
    results_table_body = get_results_table_body(browser, document)
    return locate_result_rows(browser, document, results_table_body)


# get_row_cells could be tweaked to be a standardized function
def get_row_cells(browser, document, row):
    try:
        row_cells_present = EC.presence_of_element_located((By.TAG_NAME, result_cell_tag))
        WebDriverWait(browser, timeout).until(row_cells_present)
        row_cells = row.find_elements_by_tag_name(result_cell_tag)
        return row_cells
    except TimeoutException:
        print(f'Browser timed out trying to identify row cells for '
              f'{extrapolate_document_value(document)}, please review.')


def verify_document_number(document, cells):
    if document_value(document) in map(get_element_text, cells):
        return True


def verify_book_and_page_numbers(document, cells):
    book, page = split_book_and_page(document)
    if book and page in map(get_element_text, cells):
        return True


def verify_result(document, cells):
    if document_type(document) == "document_number":
        return verify_document_number(document, cells)
    elif document_type(document) == "book_and_page":
        return verify_book_and_page_numbers(document, cells)


def check_result(browser, document, row):
    row_cells = get_row_cells(browser, document, row)
    if verify_result(document, row_cells):
        document.number_results += 1
        return True


def count_matching_results(browser, document):
    result_rows = get_result_rows(browser, document)
    for row in result_rows:
        if not check_result(browser, document, row):
            break


def get_first_row(browser, document):
    result_rows = get_result_rows(browser, document)
    return result_rows[0]


def verify_results(browser, document):
    count_matching_results(browser, document)
    if document.number_results > 0:
        get_first_row(browser, document).click()
        return True


def open_document(browser, document):
    count_total_results(browser, document)
    return verify_results(browser, document)
