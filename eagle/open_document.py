from selenium.common.exceptions import (StaleElementReferenceException,
                                        TimeoutException)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from settings.file_management import extrapolate_document_value
from settings.general_functions import naptime, short_nap, timeout

from eagle.eagle_variables import (currently_searching, failed_search,
                                   invalid_search_message, no_results_message,
                                   search_action_tag,
                                   search_actions_class_name,
                                   search_result_class_name, search_status_tag,
                                   validation_class_name)
from eagle.search import document_search, execute_search

# Use the following print statement to identify the best way to manage imports for Django vs the script folder
print("open", __name__)


def validate_search(browser, document):
    try:
        validation_message_present = EC.presence_of_element_located((By.CLASS_NAME, validation_class_name))
        WebDriverWait(browser, timeout).until(validation_message_present)
        validation_message = browser.find_element_by_class_name(validation_class_name)
        if validation_message == invalid_search_message:
            return False
        else:
            return True
    except TimeoutException:
        print(f'Browser timed out while trying to validate the search for {extrapolate_document_value(document)}')


def retry_search(browser, document):
    naptime()
    document_search(browser, document)


def get_search_status(browser):
    try:
        search_status_present = EC.presence_of_element_located((By.TAG_NAME, search_status_tag))
        WebDriverWait(browser, timeout).until(search_status_present)
        search_status = browser.find_element_by_tag_name(search_status_tag).text
        return search_status
    except TimeoutException:
        print("Browser timed out while trying to get current results.")
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


def retry_execute_search(browser, document, search_results):
    while search_results == failed_search:
        print(f'Search failed for {extrapolate_document_value(document)},'
              f' executing search again.')
        execute_search(browser)
        naptime()
        search_results = wait_for_results(browser)
    return search_results


def get_search_results(browser):
    try:
        first_result_present = EC.element_to_be_clickable((By.CLASS_NAME, search_result_class_name))
        WebDriverWait(browser, timeout).until(first_result_present)
        return browser.find_elements_by_class_name(search_result_class_name)
    except TimeoutException:
        print("Browser timed out while trying to retrieve the first result of the search.")


def count_results(browser, document):
    search_results = wait_for_results(browser)
    print(search_results)
    if search_results == failed_search or type(search_results) is None:
        print(f'Initial search failed, attempting to execute search again for '
              f'{extrapolate_document_value(document)}')
        search_results = retry_execute_search(browser, document, search_results)
    if search_results == no_results_message:
        return 0
    else:
        return int(len(get_search_results(browser)))


def check_search_results(browser, document):
    number_results = count_results(browser, document)
    document.number_results = number_results
    if number_results == 0:
        return False
    else:
        if number_results > 1:
            print(f'{number_results} documents returned while searching {extrapolate_document_value(document)}.')
        return True


def view_search_actions(browser, first_result):
    try:
        search_actions_list_present = EC.presence_of_element_located((By.CLASS_NAME, search_actions_class_name))
        WebDriverWait(browser, timeout).until(search_actions_list_present)
        search_actions_list = first_result.find_element_by_class_name(search_actions_class_name)
        return search_actions_list.find_elements_by_tag_name(search_action_tag)
    except TimeoutException:
        print("Browser timed out while trying to access search actions.")


def open_document_description(browser, first_result):
    search_actions = view_search_actions(browser, first_result)
    browser.get(search_actions[1].get_attribute("href"))


def open_document(browser, document):
    while not validate_search(browser, document):
        retry_search(browser, document)
    if check_search_results(browser, document):
        try:
            first_result = get_search_results(browser)[0]
            open_document_description(browser, first_result)
            short_nap()
            # Testing find without naptime, however hitting manual overrides more often;
            # Use short_nap if it prevents the break
            return True
        except StaleElementReferenceException:
            print(f'Encountered a stale element exception while trying to open '
                  f'{extrapolate_document_value(document)}, trying again.')
