from jaguar.validation import validate_search, verify_results_loaded
from selenium_utilities.locators import locate_element_by_class_name, locate_element_by_id

from settings.county_variables.jaguar import number_results_class_name, single_result_message, multiple_results_message, search_results_id, results_class


def count_results(browser, document):
    result_count = locate_element_by_class_name(browser, number_results_class_name,
                                                "number results", document=document)
    if result_count.text == single_result_message:
        document.number_results == 1
    elif result_count.text.endswith(multiple_results_message):
        document.number_results += int(result_count.text[:-len(multiple_results_message)])
        print(f'{document.number_results} documents returned while searching {document.extrapolate_value()}.')
    else:
        print(f'Browser unable to determine results for '
              f'{document.extrapolate_value()}, please review.')
        print("Please press enter after reviewing the search results...")
        input()


def get_results(browser, document):
    search_results_table = locate_element_by_id(browser, search_results_id,
                                                "search results table", document=document)
    # Need a separate function path if multiple results are returned
    return locate_element_by_class_name(search_results_table, results_class,
                                        "search results", True, document=document)


def open_first_result(browser, document):
    # Need a separate function path if multiple results are returned
    first_result = get_results(browser, document)


def handle_search_results(browser, document):
    if document.number_results == 0:
        return False
    elif document.number_results == 1:
        return open_first_result(browser, document)
    else:
        print(f'Search results for {document.extrapolate_value()} returned '
              f'"{document.number_results}" results, please review...')
        input()


def open_document(browser, document):
    validate_search(browser, document)
    if verify_results_loaded(browser, document):
        count_results(browser, document)
        return handle_search_results(browser, document)
    else:
        return False