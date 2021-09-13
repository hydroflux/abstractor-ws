from rattlesnake.search import locate_search_button
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from settings.file_management import extrapolate_document_value
from settings.general_functions import (get_direct_link, set_description_link,
                                        timeout)

from rattlesnake.rattlesnake_variables import results_table_id, result_row_tag_name


def locate_search_results(browser, document):
    try:
        search_results_present = EC.presence_of_element_located((By.ID, results_table_id))
        WebDriverWait(browser, timeout).until(search_results_present)
        search_results = browser.find_element_by_id(results_table_id)
        return search_results
    except TimeoutException:
        print(f'Browser timed out trying to locate search results for '
              f'{extrapolate_document_value(document)}, please review.')
        input()


def locate_search_result_rows(search_results, document):
    try:
        result_rows_present = EC.presence_of_element_located((By.TAG_NAME, result_row_tag_name))
        WebDriverWait(search_results, timeout).until(result_rows_present)
        result_rows = search_results.find_elements_by_tag_name(result_row_tag_name)
        return result_rows
    except TimeoutException:
        print(f'Browser timed out trying to locate search result rows for '
              f'{extrapolate_document_value(document)}, please review.')
        input()


def get_search_result_rows(browser, document):
    search_results = locate_search_results(browser, document)
    result_rows = locate_search_result_rows(search_results, document)
    return result_rows[1:-1]


def count_results(browser, document):
    result_rows = get_search_result_rows(browser, document)


def locate_first_result():
    pass


def get_first_result():
    pass


def open_result_link():
    pass


def open_first_result():
    pass


def handle_search_results():
    pass


def open_document():
    pass
