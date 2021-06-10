from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from settings.file_management import extrapolate_document_value
from settings.general_functions import (assert_window_title, get_element_text,
                                        timeout, update_number_results)

from crocodile.crocodile_variables import (document_description_title,
                                           link_tag, no_results_message,
                                           result_row_class_name,
                                           results_page_id,
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
        results_table_present = EC.presence_of_element_located((By.ID, results_table_id))
        WebDriverWait(browser, timeout).until(results_table_present)
        results_table = browser.find_element_by_id(results_table_id)
        return results_table
    except TimeoutException:
        print(f'Browser timed out trying to locate results for '
              f'{extrapolate_document_value(document)}, please review.')


def locate_results_statement(results_table, document):
    try:
        results_statement_present = EC.presence_of_element_located((By.TAG_NAME, results_statement_tag))
        WebDriverWait(results_table, timeout).until(results_statement_present)
        results_statement = results_table.find_element_by_tag_name(results_statement_tag)
        return get_element_text(results_statement)
    except TimeoutException:
        print(f'Browser timed out trying to locate results statement for '
              f'{extrapolate_document_value(document)}, please review.')


def strip_total_search_results(results_statement):
    return int(results_statement[(results_statement.find("of") + 2):results_statement.find("at")].strip())


def count_total_search_results(results_table, document):
    results_statement = locate_results_statement(results_table, document)
    total_search_results = strip_total_search_results(results_statement)
    return total_search_results


def locate_result_rows(results_table, document):
    try:
        result_rows_present = EC.presence_of_element_located((By.CLASS_NAME, result_row_class_name))
        WebDriverWait(results_table, timeout).until(result_rows_present)
        result_rows = results_table.find_elements_by_class_name(result_row_class_name)
        return result_rows
    except TimeoutException:
        print(f'Browser timed out trying to locate results for '
              f'{extrapolate_document_value(document)}, please review.')


def verify_result_count(document, total_search_results, results):
    if not len(results) == total_search_results:
        print(f'The total result count of {total_search_results} does not match the number of rows for '
              f'{extrapolate_document_value(document)}, which returned '
              f'{len(results)}, please review.')


def locate_document_link(row, document):
    try:
        document_link_present = EC.element_to_be_clickable((By.TAG_NAME, link_tag))
        WebDriverWait(row, timeout).until(document_link_present)
        document_link = row.find_element_by_tag_name(link_tag)
        return document_link
    except TimeoutException:
        print(f'Browser timed out trying to open document link for '
              f'{extrapolate_document_value(document)}, please review.')


def open_document_link(row, document):
    document_link = locate_document_link(row, document)
    document_link.click()


def handle_search_results(result_rows, document):
    if document.number_results == 1:
        open_document_link(result_rows[0], document)
    else:
        print(f'{str(document.number_results)} results returned for '
              f'{extrapolate_document_value(document)}, please review.')
        # Need to create an application path for multiple results


def open_document(browser, document):
    if check_for_results(browser, document):
        results_table = locate_search_results_table(browser, document)
        total_search_results = count_total_search_results(results_table, document)
        result_rows = locate_result_rows(results_table, document)
        verify_result_count(document, total_search_results, result_rows)
        handle_search_results(result_rows, document)
        if assert_window_title(browser, document_description_title):
            return True
        else:
            print(f'Browser failed to successfully open document description page for '
                  f'{extrapolate_document_value(document)}, please review.')
