from selenium.common.exceptions import (StaleElementReferenceException,
                                        TimeoutException)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# Use the following print statement to identify the best way to manage imports for Django vs the script folder
print("open", __name__)

from settings.file_management import document_type, document_value
from settings.general_functions import naptime
from settings.settings import timeout

from eagle.eagle_variables import (first_result_class_name, first_result_tag,
                                   search_action_tag,
                                   search_actions_class_name)


def get_first_result(browser):
    try:
        first_result_present = EC.presence_of_element_located((By.CLASS_NAME, first_result_class_name))
        WebDriverWait(browser, timeout).until(first_result_present)
        return browser.find_element_by_class_name(first_result_class_name)
    except TimeoutException:
        print("Browser timed out while trying to retrieve the first result of the search.")


def get_first_result_info(browser):
    first_result = get_first_result(browser)
    first_result_info = first_result.find_element_by_tag_name(first_result_tag)
    browser.execute_script("arguments[0].scrollIntoView();", first_result_info)
    return first_result_info


def verify_first_result_number(document, first_result_info):
    return first_result_info.text.split(" ")[0] == document.value


def verify_first_result_book_and_page(document, first_result_info):
    pass


def verify_result(browser, document):
    first_result_info = get_first_result_info(browser)
    if document_type(document) == "document_number":
        return verify_first_result_number(document, first_result_info)
    elif document_type(document) == "book_and_page":
        return verify_first_result_book_and_page(document, first_result_info)


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


def determine_document_status(browser, document):
    if verify_result(browser, document):
        print(f'Document {document_value(document)} matches the search result, moving forward.')
        open_document_description(browser, get_first_result(browser))
        naptime()
        return True
    else:
        print(f'Document number {document_value(document)} not found -- document number '
              f'{first_result_number(browser)} returned as top search result.')
        return False


def open_document(browser, document):
    try:
        return determine_document_status(browser, document)
    except StaleElementReferenceException:
        print(f'Encountered a stale element exception while trying to open {document_value(document)}, trying again.')
        browser.refresh()
        return determine_document_status(browser, document)
