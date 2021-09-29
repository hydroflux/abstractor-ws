from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from selenium_utilities.open import assert_window_title

from settings.classes.Document import Document
from settings.county_variables.crocodile import (document_description_title,
                                                 filter_list, link_tag,
                                                 no_results_message,
                                                 results_page_id,
                                                 results_statement_tag,
                                                 results_table_id)
from settings.file_management import document_value, extrapolate_document_value
from settings.general_functions import (get_direct_children, get_direct_link,
                                        get_element_text,
                                        javascript_script_execution,
                                        set_description_link, timeout)


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


def locate_main_results_table(browser, document):
    try:
        results_table_present = EC.presence_of_element_located((By.ID, results_table_id))
        WebDriverWait(browser, timeout).until(results_table_present)
        results_table = browser.find_element_by_id(results_table_id)
        return results_table
    except TimeoutException:
        print(f'Browser timed out trying to locate results for '
              f'{extrapolate_document_value(document)}, please review.')


def locate_search_results_table(main_table, document):
    pass


def get_search_results(main_table):
    return get_direct_children(get_direct_children(main_table)[2])


def verify_result_count(total_search_results, search_results, document):
    if not len(search_results) == total_search_results:
        print(f'The total result count of {total_search_results} does not match the number of rows for '
              f'{extrapolate_document_value(document)}, which returned '
              f'{len(search_results)}, please review.')


def list_search_results(browser, document):
    main_table = locate_main_results_table(browser, document)
    total_results = count_total_results(main_table, document)
    search_results = get_search_results(main_table)
    verify_result_count(total_results, search_results, document)
    return search_results


def locate_results_statement(results_table, document):
    try:
        results_statement_present = EC.presence_of_element_located((By.TAG_NAME, results_statement_tag))
        WebDriverWait(results_table, timeout).until(results_statement_present)
        results_statement = results_table.find_element_by_tag_name(results_statement_tag)
        return get_element_text(results_statement)
    except TimeoutException:
        print(f'Browser timed out trying to locate results statement for '
              f'{extrapolate_document_value(document)}, please review.')


def strip_total_results(results_statement):
    return int(results_statement[(results_statement.find("of") + 2):results_statement.find("at")].strip())


def count_total_results(main_table, document):
    results_statement = locate_results_statement(main_table, document)
    total_results = strip_total_results(results_statement)
    return total_results


def get_result_number(result):
    # Create a similar function for matching book / page numbers
    return get_direct_children(result)[8]


def locate_document_description_link(result_number, document):
    try:
        document_description_link_present = EC.element_to_be_clickable((By.TAG_NAME, link_tag))
        WebDriverWait(result_number, timeout).until(document_description_link_present)
        document_description_link = result_number.find_element_by_tag_name(link_tag)
        return document_description_link
    except TimeoutException:
        print(f'Browser timed out trying to open document link for '
              f'{extrapolate_document_value(document)}, please review.')


def get_document_description_link(result_number, document):
    document_description_link = get_direct_link(locate_document_description_link(result_number, document))
    if document.description_link is None:
        set_description_link(document, document_description_link)
    elif type(document.description_link) == str:
        document.description_link = [document.description_link, document_description_link]
    elif type(document_description_link) == list:
        document.description_link = [*document.description_link, document_description_link]


def verify_search_results(search_results, document):
    for result in search_results:
        result_number = get_result_number(result)
        if document_value(document) == get_element_text(result_number):
            get_document_description_link(result_number, document)
            document.number_results += 1


def open_document_link(browser, link):
    javascript_script_execution(browser, link)
    if not assert_window_title(browser, document_description_title):
        print(f'Browser failed to return to "{document_description_title}" page, trying again.')
        browser.back()
        # short_nap()
        javascript_script_execution(browser, link)
    # Overall not a great combination of functions, need to slow everything down to see where the issue is occuring


def next_result(browser, document, index):
    count = 0
    while not assert_window_title(browser, document_description_title):
        browser.back()
        # short_nap()
        count += 1
        if count == 10:
            break
    open_document_link(browser, document.description_link[index + 1])


def handle_search_results(browser, document):
    if document.number_results == 1:
        open_document_link(browser, document.description_link)
    else:
        print(f'{extrapolate_document_value(document)} returned '
              f'{str(document.number_results)} results, recording each to dataframe for review.')
        open_document_link(browser, document.description_link[0])
        # If number_results == 0
        # do something
        # elif number_results > 1
        # do something
        # Need to create an application path for multiple results


def get_result_type(result):
    return get_element_text(get_direct_children(result)[2])


def filter_search_results(result_list, result):
    if get_result_type(result) not in filter_list:
        search_result = get_element_text(get_result_number(result))
        if search_result not in result_list:
            result_list.append(search_result)


def aggregate_search_results(search_results):
    result_list = []
    for result in search_results:
        filter_search_results(result_list, result)
    return result_list


def transform_result_list(result_list):
    document_list = []
    for result in result_list:
        document_list.append(Document(type="document_number", value=result))
    return document_list


def create_name_document_list(browser, search_name):
    if check_for_results(browser, search_name):
        search_results = list_search_results(browser, search_name)
        result_list = aggregate_search_results(search_results)
        return transform_result_list(result_list)
    else:
        print(f'No results found for '
              f'{extrapolate_document_value(search_name)} '
              f'please review search criteria & try again.')
        browser.quit()
        exit()


def open_document(browser, document):
    if check_for_results(browser, document):
        search_results = list_search_results(browser, document)
        verify_search_results(search_results, document)
        handle_search_results(browser, document)
        if assert_window_title(browser, document_description_title):
            #  Moving to open_document_link, making this redundant, but need to decide how to handle
            #  the else: statement
            return True
        else:
            print(f'Browser failed to successfully open document description page for '
                  f'{extrapolate_document_value(document)}, please review.')
