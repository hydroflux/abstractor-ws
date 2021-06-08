from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from settings.file_management import (document_type, document_value,
                                      extrapolate_document_value)
from settings.general_functions import (get_element_text, timeout,
                                        update_number_results)

from crocodile.crocodile_variables import (no_results_message, results_page_id,
                                           results_statement_tag,
                                           results_table_id)


def locate_results_page_information(browser, document):
    try:
        results_page_present = EC.presence_of_element_located((By.ID, results_page_id))
        WebDriverWait(browser, timeout).until(results_page_present)
        results_page = browser.find_element_by_id(results_page_id)
        return get_element_text(results_page)
    except TimeoutException:
        print(f'Browser timed out trying to locate results page information for '
              f'{extrapolate_document_value(document)}, please review.')


def check_for_results(browser, document):
    results_page_information = locate_results_page_information(browser, document)
    if results_page_information.startswith(no_results_message):
        print(f'{no_results_message} for {extrapolate_document_value(document)}')
        return False
    else:
        return True


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
        return get_element_text(results_statement)
    except TimeoutException:
        print(f'Browser timed out trying to locate results statement for '
              f'{extrapolate_document_value(document)}, please review.')


def strip_total_results(results_statement):
    return results_statement[(results_statement.find("of") + 2):results_statement.find("at")].strip()


def count_total_results(browser, results_table, document):
    results_statement = locate_results_statement(browser, results_table, document)
    total_results = strip_total_results(results_statement)
    update_number_results(document, total_results)
    return total_results


def open_document_link(browser):
    pass


def open_document(browser, document):
    if check_for_results(browser):
        results_table = locate_search_results_table(browser, document)
        count_total_results(browser, results_table, document)
        # return verify_results(browser, document)
