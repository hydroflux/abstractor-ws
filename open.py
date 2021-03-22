from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from variables import timeout, first_result_class_name, search_actions_class_name

def get_first_result(browser):
    try:
        first_result_present = EC.presence_of_element_located((By.CLASS_NAME, first_result_class_name))
        WebDriverWait(browser, timeout).until(first_result_present)
        first_result = browser.find_element_by_class_name(first_result_class_name)
        return first_result
    except TimeoutException:
        print("Browser timed out while trying to retrieve the first result of the search.")

def result_number(browser):
    first_result = get_first_result(browser)
    first_result_head = first_result.find_element_by_tag_name("h1").text
    result_number = first_result_head_text.split(" ")[0]
    return result_number

def verify_result(document_number):
    result_number(browser) == document_number

def open_document_description(browser, first_result):
    search_actions_list = first_result.find_element_by_class_name(search_actions_class_name)
    search_actions = search_actions_list.find_elements_by_tag_name("a")
    view_document = search_actions[1]
    view_document.click()

def open_document(browser, document_number):
    if verify_result(document_number):
        first_result = get_first_result(browser)
        first_result.click()
        f'Document number {document_number} matches the search result, moving forward.'
        open_document_description(browser, first_result)
        return True
    else:
        print(f'Document number {document_number} not found -- document number {result_number(browser)} returned as top search result.')
        return False
