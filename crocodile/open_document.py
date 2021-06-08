from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from settings.file_management import (document_type, document_value,
                                      extrapolate_document_value)
from settings.general_functions import get_element_text, timeout

from crocodile.crocodile_variables import results_table_id, results_statement_tag



def locate_search_results_table(browser, document):
    try:
        results_present = EC.presence_of_element_located((By.ID, results_table_id))
        WebDriverWait(browser, timeout).until(results_present)
        results = browser.find_element_by_id(results_table_id)
        return results
    except TimeoutException:
        print(f'Browser timed out trying to locate results for '
              f'{extrapolate_document_value(document)}, please review.')


def locate_results_statement(browser, results_table, document):
    try:
        results_statement_present = EC.presence_of_element_located((By.TAG_NAME, results_statement_tag))
        WebDriverWait(results_table, timeout).until(results_statement_present)
        results_statement = results_table.find_element_by_tag_name(results_statement_tag)
        return results_statement
    except TimeoutException:
        print(f'Browser timed out trying to locate results statement for '
              f'{extrapolate_document_value(document)}, please review.')


def count_total_results(browser, results_table, document):
    results_statement = locate_results_statement(browser, results_table, document)
    print(results_statement.text)


def open_document_link(browser):
    pass


def verify_results(browser, document):
    pass


def open_document(browser, document):
    results_table = locate_search_results_table(browser, document)
    count_total_results(browser, results_table, document)
    return verify_results(browser, document)
