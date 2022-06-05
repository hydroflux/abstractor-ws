from selenium_utilities.locators import (locate_element_by_class_name,
                                         locate_elements_by_class_name)
from settings.general_functions import javascript_script_execution


def count_results(browser, abstract, document):
    result_count_container = locate_elements_by_class_name(browser, abstract.county.classes["Result Count Container"],
                                                           "result count container", False, document)[1]
    result_count_text = result_count_container.text.split('\n')[1]
    document.number_results = int(result_count_text.split(' ')[-2])


def access_result_rows(browser, abstract, document):
    return locate_elements_by_class_name(browser, abstract.county.classes["Result Row"], "result rows", False, document)


def access_result_button(browser, abstract, document, result_rows):
    result = result_rows[document.result_number]
    result_button = locate_element_by_class_name(result, abstract.county.buttons['Open Document'],
                                                 "result button", True, document)
    return result_button.get_attribute('href')


def get_results(browser, abstract, document):
    count_results(browser, abstract, document)
    result_rows = access_result_rows(browser, abstract, document)
    result_links = []
    for result in result_rows:
        document.result_number = result_rows.index(result)
        result_link = access_result_button(browser, abstract, document, result_rows)
        result_links.append(result_link)
    document.result_number = 0
    return result_links


def open_result(browser, abstract, document, result):
    if result:
        javascript_script_execution(browser, result)
    else:
        result_rows = access_result_rows(browser, abstract, document)
        result_link = access_result_button(browser, abstract, document, result_rows)
        javascript_script_execution(browser, result_link)


# Not currently in use (only legal search set up)
def open_document(browser, abstract, document):
    if not document.number_results:
        count_results(browser, abstract, document)
    open_result(browser, abstract, document)
