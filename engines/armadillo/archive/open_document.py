from selenium.common.exceptions import TimeoutException

from selenium_utilities.locators import (locate_element_by_class_name,
                                         locate_element_by_id,
                                         locate_element_by_tag_name,
                                         locate_elements_by_class_name)
from settings.county_variables.armadillo import (link_tag,
                                                 multiple_results_message,
                                                 number_results_class,
                                                 result_class_names,
                                                 search_results_id,
                                                 single_result_message)
from settings.general_functions import get_direct_link

from engines.armadillo.validation import (validate_result,
                                          verify_results_loaded,
                                          verify_search_results_page_loaded)


def count_results(browser, document):
    result_count = locate_element_by_class_name(browser, number_results_class, "number results", document=document)
    if result_count.text == single_result_message:
        document.number_results += 1
    elif result_count.text.endswith(multiple_results_message):
        document.number_results += int(result_count.text[:-len(multiple_results_message)])
        print(f'{document.number_results} documents returned while searching {document.extrapolate_value()}.')
    else:
        print(f'Browser unable to determine results for '
              f'{document.extrapolate_value()}, please review.')
        print("Please press enter after reviewing the search results...")
        input()


def determine_results_class(result_number):
    return result_class_names[result_number % 2]


def get_results(browser, document, result_number):
    search_results_table = locate_element_by_id(browser, search_results_id,
                                                "search results table", document=document)
    results_class = determine_results_class(result_number)
    return locate_elements_by_class_name(search_results_table, results_class,
                                         "search results", True, document=document)


def access_result(browser, document, result_number):
    results = get_results(browser, document, result_number)
    return results[int(result_number/2)]


def access_result_link(document, result):
    result_link_element = locate_element_by_tag_name(result, link_tag, "result link", True, document)
    return get_direct_link(result_link_element)


# Does this need a try / exception to function properly?
def open_result_link(browser, document, result):
    try:
        document_link = access_result_link(document, result)
        document.description_link = document_link
        browser.get(document.description_link)
        return True
    except TimeoutException:
        print(f'Browser timed out trying to open result link for '
              f'{document.extrapolate_value()}, please review.')
        input()
        return False


def open_result(browser, document, result_number):
    result = access_result(browser, document, result_number)
    result_text = result.text.split('\n')
    if validate_result(result_text, document):
        return open_result_link(browser, document, result)
    else:
        return False


def handle_document_search(browser, document, result_number):
    if document.number_results == 0:
        return False
    else:
        return open_result(browser, document, result_number)


def open_document(browser, document, result_number=0):
    verify_search_results_page_loaded(browser, document)
    if verify_results_loaded(browser, document):
        if result_number == 0:
            count_results(browser, document)
        return handle_document_search(browser, document, result_number)
    else:
        return False
