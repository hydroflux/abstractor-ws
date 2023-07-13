from selenium.common.exceptions import (StaleElementReferenceException,
                                        TimeoutException)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from project_management.timers import naptime, short_nap, timeout

from selenium_utilities.locators import (locate_element_by_class_name,
                                         locate_elements_by_class_name,
                                         locate_elements_by_tag_name)
from selenium_utilities.open import open_url

from settings.general_functions import get_direct_link

from engines.eagle.search import execute_search, search

# Use the following print statement to identify the best way to manage imports for Django vs the script folder
print("open", __name__)


def validate_search(browser, abstract, document):
    return (abstract.county.messages["Invalid Search"] !=
            locate_element_by_class_name(browser, abstract.county.classes["Validation"],
                                         "search validation message", document=document))


def retry_search(browser, abstract, document):
    browser.refresh()
    naptime()
    search(browser, abstract, document)


def get_search_status(browser, abstract):
    try:
        search_status_present = EC.presence_of_element_located((By.TAG_NAME, abstract.county.tags["Search Status"]))
        WebDriverWait(browser, timeout).until(search_status_present)
        search_status = browser.find_element("tag name", abstract.county.tags["Search Status"]).text
        return search_status
    except TimeoutException:
        print("Browser timed out trying to get current results.")
    except StaleElementReferenceException:
        print('Encountered a stale element reference exception trying to determine search status, '
              'refreshing & trying again.')
        browser.refresh()
        naptime()
        return None


def wait_for_results(browser, abstract):
    search_status = get_search_status(browser, abstract)
    while search_status == abstract.county.messages["Currently Searching"] or search_status is None:
        short_nap()
        search_status = get_search_status(browser, abstract)
    return search_status


def retry_execute_search(browser, abstract, document, search_status):
    count = 0
    while search_status == abstract.county.messages["Failed Search"]:
        print(f'Search failed for {document.extrapolate_value()},'
              f' executing search again.')
        execute_search(browser, abstract, document)
        naptime()
        search_status = wait_for_results(browser, abstract)
        count += 1
        # Changed from 5 on 07/12/2023
        if count == 3:
            input("Unable to complete search, please review and press enter after making adjustments...")
    return search_status


def get_search_results(browser, abstract, document):
    result_rows = locate_elements_by_class_name(browser, abstract.county.classes["Results Row"],
                                                "search results", True, document=document)
    while result_rows is None:
        retry_search(browser, abstract, document)
        result_rows = locate_elements_by_class_name(browser, abstract.county.classes["Results Row"],
                                                    "search results", True, document=document)
    return result_rows


def count_results(browser, abstract, document):
    # try:
    result_rows = get_search_results(browser, abstract, document)
    if result_rows is not False:
        document.number_results += len(result_rows)
    # Again, I don't think the try / exception is necessary here
    # return int(number_results)
    # except TypeError:
    #     print(f'Encountered a "TypeError" trying to count search results for '
    #           f'{document.extrapolate_value()}, please review.')
    #     return None


def handle_result_count(browser, abstract, document):
    search_status = wait_for_results(browser, abstract)
    if search_status == abstract.county.messages["Failed Search"]:
        print(f'Initial search failed, attempting to execute search again for '
              f'{document.extrapolate_value()}')
        search_status = retry_execute_search(browser, abstract, document, search_status)
    if search_status == abstract.county.messages["No Results"]:
        print(f'No results located at {document.extrapolate_value()}, please review.')
    else:
        count_results(browser, abstract, document)


def check_search_results(browser, abstract, document):
    handle_result_count(browser, abstract, document)
    # number_results = process_result_count_from_search(browser, document)
    if document.number_results == 0:
        return False
    else:
        if document.number_results > 1:
            print(f'{document.number_results} documents returned while searching '
                  f'{document.extrapolate_value()}.')
        return True


def get_document_link(abstract, result, document):
    result_actions_list = locate_element_by_class_name(result, abstract.county.classes["Result Actions"],
                                                       "search results actions list", document=document)
    return locate_elements_by_tag_name(result_actions_list, abstract.county.tags["Result Actions"],
                                       "search actions", document=document)[1]


def open_document_description(browser, abstract, document, result):
    document_link = get_document_link(abstract, result, document)
    document.description_link = get_direct_link(document_link)
    open_url(browser, document.description_link, abstract.county.titles["Document Description"],
             "document description", document)


def handle_document_search(browser, abstract, document):
    try:
        first_result = get_search_results(browser, abstract, document)[0]
        open_document_description(browser, abstract, document, first_result)
        short_nap()  # W/O nap pdf fails to load properly on first try
        return True
    except StaleElementReferenceException:
        print(f'Encountered a stale element exception while trying to open '
              f'{document.extrapolate_value()}, trying again.')


def open_document(browser, abstract, document):
    while not validate_search(browser, abstract, document):
        retry_search(browser, abstract, document)
    if check_search_results(browser, abstract, document):
        return handle_document_search(browser, abstract, document)
