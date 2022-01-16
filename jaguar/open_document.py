from selenium_utilities.locators import (locate_element_by_class_name,
                                         locate_element_by_id,
                                         locate_element_by_tag_name)
from selenium_utilities.open import open_url

from settings.county_variables.jaguar import (document_description_title,
                                              link_tag,
                                              multiple_results_message,
                                              number_results_class_name,
                                              results_class, search_results_id,
                                              single_result_message)
from settings.general_functions import get_direct_link

from jaguar.validation import (validate_result, validate_search,
                               verify_results_loaded)


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
                                        "search results", True, document)


def access_result_link(document, result):
    result_link_element = locate_element_by_tag_name(result, link_tag, "result link", True, document)
    return get_direct_link(result_link_element)


def open_result_link(browser, document, result):
    document_link = access_result_link(document, result)
    return open_url(browser, document_link, document_description_title,
                    "document description", document)


def open_first_result(browser, document):
    # Need a separate function path if multiple results are returned
    first_result = get_results(browser, document)
    if validate_result(first_result, document):
        return open_result_link(browser, document, first_result)
    else:
        return False


# Very similar to armadillo 'handle_search_results' dependent functions
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
