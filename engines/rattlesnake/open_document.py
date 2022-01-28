from selenium.common.exceptions import TimeoutException

from selenium_utilities.locators import (locate_element_by_id,
                                         locate_element_by_tag_name,
                                         locate_elements_by_tag_name)

from settings.county_variables.rattlesnake import (result_link_tag_name,
                                                   result_row_tag_name,
                                                   results_table_id)
from settings.general_functions import (get_direct_link,
                                        javascript_script_execution)

from rattlesnake.validation import (validate_result_reception_number,
                                    validate_result_volume_and_page_numbers)


# Search results can also be used to identify the number of results pages
def get_search_result_rows(browser, document):
    search_results = locate_element_by_id(browser, results_table_id,
                                          "search results", document=document)
    result_rows = locate_elements_by_tag_name(search_results, result_row_tag_name,
                                              "search result rows", document=document)
    return result_rows[1:-1]


def count_results(browser, document):
    result_rows = get_search_result_rows(browser, document)
    for _ in result_rows:
        document.number_results += 1
    if document.number_results > 1:
        print(f'{document.number_results} documents returned while searching {document.extrapolate_value()}.')


def get_result(browser, document, result_number=0):
    return get_search_result_rows(browser, document)[result_number]


def get_result_link(result, document):
    result_link_element = locate_element_by_tag_name(result, result_link_tag_name, "result link",
                                                     True, document=document)
    return get_direct_link(result_link_element)


def open_result_link(browser, document, result):
    try:
        document_link = get_result_link(result, document)
        document.description_link = document_link
        javascript_script_execution(browser, document.description_link)
        return True
    except TimeoutException:
        print(f'Browser timed out trying to open result link for '
              f'{document.extrapolate_value()}, please review')
        input()
        return False


def handle_result_document_type(browser, result, document):
    if document.type == 'document_number' and validate_result_reception_number(result, document):
        return open_result_link(browser, document, result)
    elif document.type == 'volume_and_page' and validate_result_volume_and_page_numbers(result, document):
        return open_result_link(browser, document, result)
    else:
        print(f'Browser encountered issues validating document type '
              f'"{document.type}" for "{document.document_value()}", please review.')
        input()


def open_result(browser, document, result_number):
    result = get_result(browser, document, result_number)
    return handle_result_document_type(browser, result, document)


def handle_search_results(browser, document, result_number):
    if document.number_results == 0:
        return False
    else:
        return open_result(browser, document, result_number)


def open_document(browser, document, result_number=0):
    if result_number == 0:
        count_results(browser, document)
    return handle_search_results(browser, document, result_number)
