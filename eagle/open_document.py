from selenium.common.exceptions import (NoSuchElementException,
                                        StaleElementReferenceException,
                                        TimeoutException)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# Use the following print statement to identify the best way to manage imports for Django vs the script folder
print("open", __name__)

from settings.file_management import (document_type, document_value,
                                      extrapolate_document_value)
from settings.general_functions import naptime
from settings.settings import timeout

from eagle.eagle_variables import (book_and_page_tag, book_title,
                                   first_result_class_name,
                                   first_result_submenu_class,
                                   first_result_tag, nested_submenu_class,
                                   page_title, search_action_tag,
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


def get_first_result_nested_info(browser, first_result_info):
    try:
        first_result_nested_info_present = EC.presence_of_element_located((By.CLASS_NAME, first_result_submenu_class))
        WebDriverWait(browser, timeout).until(first_result_nested_info_present)
        first_result_nested_info = browser.find_elements_by_class_name(first_result_submenu_class)
        return first_result_nested_info
    except TimeoutException:
        print(f'Browser timed out while trying to get nested information from "{first_result_info.text}".')


def split_book_and_page_info(book_and_page_info):
    book_and_page_values = book_and_page_info[-1].text.split()
    if book_and_page_values[0] == book_title and book_and_page_values[2] == page_title:
        return [book_and_page_values[1], book_and_page_values[3]]
    else:
        print(f'Book & page titles do not line up as expected, instead got "{book_and_page_values}", please review.')
        return False


def expand_first_result_nested_info(browser, first_result_info):
    try:
        browser.find_element_by_class_name(nested_submenu_class)
    except NoSuchElementException:
        first_result_info.click()


def get_book_and_page_values(browser, first_result_info):
    expand_first_result_nested_info(browser, first_result_info)
    nested_info = get_first_result_nested_info(browser, first_result_info)
    book_and_page_info = nested_info[-1].find_elements_by_tag_name(book_and_page_tag)
    return split_book_and_page_info(book_and_page_info)


def get_first_result_value(browser, document):
    first_result_info = get_first_result_info(browser)
    if document_type(document) == "document_number":
        return first_result_info.text.split(" ")[0]
    elif document_type(document) == "book_and_page":
        return get_book_and_page_values(browser, first_result_info)


def verify_first_result_number(document, first_result_value):
    return first_result_value == document_value(document)


def verify_first_result_book_and_page(document, first_result_value):
    if first_result_value is not False:
        book = first_result_value[0]
        page = first_result_value[1]
        if book == document_value(document)[0] and page == document_value(document)[1]:
            return True
        else:
            print("")
            return False
    else:
        return False


def verify_result(browser, document):
    first_result_value = get_first_result_value(browser, document)
    if document_type(document) == "document_number":
        return verify_first_result_number(document, first_result_value)
    elif document_type(document) == "book_and_page":
        return verify_first_result_book_and_page(document, first_result_value)


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
        print(f'{extrapolate_document_value(document)} matches the search result, moving forward.')
        open_document_description(browser, get_first_result(browser))
        naptime()
        return True
    else:
        print(f'{extrapolate_document_value(document)} not found -- '
              f'{get_first_result_value(browser, document)} returned as top search result.')
        return False


def open_document(browser, document):
    try:
        return determine_document_status(browser, document)
    except StaleElementReferenceException:
        print(f'Encountered a stale element exception while trying to open '
              f'{extrapolate_document_value(document)}, trying again.')
        browser.refresh()
        return determine_document_status(browser, document)
