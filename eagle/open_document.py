from selenium.common.exceptions import (StaleElementReferenceException,
                                        TimeoutException)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from selenium_utilities.locators import (locate_element_by_class_name,
                                         locate_elements_by_class_name,
                                         locate_elements_by_tag_name)
from selenium_utilities.open import open_url

from settings.county_variables.eagle import (currently_searching,
                                             document_description_title,
                                             failed_search,
                                             invalid_search_message,
                                             no_results_message,
                                             result_action_tag_name,
                                             result_actions_class_name,
                                             results_row_class_name,
                                             search_status_tag,
                                             validation_class_name)
from settings.general_functions import (get_direct_link, naptime, short_nap,
                                        timeout)

from eagle.search import execute_search, search

# Use the following print statement to identify the best way to manage imports for Django vs the script folder
print("open", __name__)


def validate_search(browser, document):
    return invalid_search_message != locate_element_by_class_name(browser, validation_class_name,
                                                                  "search validation message", document=document)


def retry_search(browser, document):
    browser.refresh()
    naptime()
    search(browser, document)


def get_search_status(browser):
    try:
        search_status_present = EC.presence_of_element_located((By.TAG_NAME, search_status_tag))
        WebDriverWait(browser, timeout).until(search_status_present)
        search_status = browser.find_element_by_tag_name(search_status_tag).text
        return search_status
    except TimeoutException:
        print("Browser timed out trying to get current results.")
    except StaleElementReferenceException:
        print('Encountered a stale element reference exception trying to determine search status, '
              'refreshing & trying again.')
        browser.refresh()
        naptime()
        return None


def wait_for_results(browser):
    search_status = get_search_status(browser)
    while search_status == currently_searching or search_status is None:
        short_nap()
        search_status = get_search_status(browser)
    return search_status


def retry_execute_search(browser, document, search_status):
    while search_status == failed_search:
        print(f'Search failed for {document.extrapolate_value()},'
              f' executing search again.')
        execute_search(browser)
        naptime()
        search_status = wait_for_results(browser)
    return search_status


# def locate_first_result(browser):
#     try:
#         first_result_present = EC.element_to_be_clickable((By.CLASS_NAME, search_result_class_name))
#         WebDriverWait(browser, timeout).until(first_result_present)
#         first_result = browser.find_elements_by_class_name(search_result_class_name)
#         return first_result
#     except TimeoutException:
#         print("Browser timed out trying to retrieve the first result of the search.")


def get_search_results(browser, document):
    result_rows = locate_elements_by_class_name(browser, results_row_class_name,
                                                "search results", True, document=document)
    while type(result_rows) is None:
        retry_search(browser, document)
        result_rows = locate_elements_by_class_name(browser, results_row_class_name,
                                                    "search results", True, document=document)
    return result_rows


def count_results(browser, document):
    # try:
    result_rows = get_search_results(browser, document)
    document.number_results += len(result_rows)
    # Again, I don't think the try / exception is necessary here
    # return int(number_results)
    # except TypeError:
    #     print(f'Encountered a "TypeError" trying to count search results for '
    #           f'{document.extrapolate_value()}, please review.')
    #     return None


def handle_result_count(browser, document):
    search_status = wait_for_results(browser)
    if search_status == failed_search:
        print(f'Initial search failed, attempting to execute search again for '
              f'{document.extrapolate_value()}')
        search_status = retry_execute_search(browser, document, search_status)
    if search_status == no_results_message:
        print(f'No results located at {document.extrapolate_value()}, please review.')
    else:
        count_results(browser, document)


# def process_result_count_from_search(browser, document):
#     while document.number_results is None:
#         print(f'Result count returned "None" for '
#               f'{document.extrapolate_value()}, attempting to execute search again.')
#         retry_search(browser, document)  # Should correct for TypeError; doesn't account for fill_search_field failing
#         result_count = handle_result_count(browser, document)
#     return result_count


def check_search_results(browser, document):
    handle_result_count(browser, document)
    # number_results = process_result_count_from_search(browser, document)
    if document.number_results == 0:
        return False
    else:
        if document.number_results > 1:
            print(f'{document.number_results} documents returned while searching {document.extrapolate_value()}.')
        return True


# def view_search_actions(browser, result):
#     try:
#         search_actions_list_present = EC.presence_of_element_located((By.CLASS_NAME, search_actions_class_name))
#         WebDriverWait(browser, timeout).until(search_actions_list_present)
#         search_actions_list = result.find_element_by_class_name(search_actions_class_name)
#         return search_actions_list.find_elements_by_tag_name(search_action_tag_name)
#     except TimeoutException:
#         print("Browser timed out while trying to access search actions.")


def get_document_link(result, document):
    result_actions_list = locate_element_by_class_name(result, result_actions_class_name,
                                                       "search results actions list", document=document)
    return locate_elements_by_tag_name(result_actions_list, result_action_tag_name,
                                       "search actions", document=document)[1]


def open_document_description(browser, document, result):
    document_link = get_document_link(result, document)
    document.description_link = get_direct_link(document_link)
    open_url(browser, document.description_link, document_description_title, "document description", document)


def handle_search_results(browser, document):
    try:
        first_result = get_search_results(browser, document)[0]
        open_document_description(browser, document, first_result)
        short_nap()  # W/O nap pdf fails to load properly on first try
        return True
    except StaleElementReferenceException:
        print(f'Encountered a stale element exception while trying to open '
              f'{document.extrapolate_value()}, trying again.')


def open_document(browser, document):
    while not validate_search(browser, document):
        retry_search(browser, document)
    if check_search_results(browser, document):
        return handle_search_results(browser, document)
