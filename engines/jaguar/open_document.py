from engines.jaguar.validation import (validate_result, validate_search,
                                       verify_results_loaded)

from selenium_utilities.locators import (locate_element_by_class_name,
                                         locate_element_by_id,
                                         locate_element_by_tag_name)
from selenium_utilities.open import open_url

from settings.general_functions import get_direct_link


def count_results(browser, abstract, document):
    result_count = locate_element_by_class_name(browser, abstract.county.classes["Number Results"],
                                                "number results", document=document)
    if result_count.text == abstract.county.messages["Single Result"]:
        document.number_results = 1
    elif result_count.text.endswith(abstract.county.messages["Multiple Results"]):
        document.number_results += int(result_count.text[:-len(abstract.county.messages["Multiple Results"])])
        print(f'{document.number_results} documents returned while searching {document.extrapolate_value()}.')
    else:
        print(f'Browser unable to determine results for '
              f'{document.extrapolate_value()}, please review.')
        print("Please press enter after reviewing the search results...")
        input()


def get_results(browser, abstract, document):
    search_results_table = locate_element_by_id(browser, abstract.county.ids["Search Results"],
                                                "search results table", document=document)
    # Need a separate function path if multiple results are returned
    return locate_element_by_class_name(search_results_table, abstract.county.classes["Results"],
                                        "search results", True, document)


def access_result_link(abstract, document, result):
    result_link_element = locate_element_by_tag_name(result, abstract.county.tags["Link"],
                                                     "result link", True, document)
    return get_direct_link(result_link_element)


def open_result_link(browser, abstract, document, result):
    document_link = access_result_link(abstract, document, result)
    open_url(browser, document_link, abstract.county.titles["Document Description"],
             "document description", document)
    return True


def open_first_result(browser, abstract, document):
    # Need a separate function path if multiple results are returned
    first_result = get_results(browser, abstract, document)
    if validate_result(document, first_result):
        return open_result_link(browser, abstract, document, first_result)
    else:
        return False


# Very similar to armadillo 'handle_search_results' dependent functions
def handle_document_search(browser, abstract, document):
    if document.number_results == 0:
        return False
    elif document.number_results == 1:
        return open_first_result(browser, abstract, document)
    else:
        print(f'Search results for {document.extrapolate_value()} returned '
              f'"{document.number_results}" results, please review...')
        input()


def open_document(browser, abstract, document):
    validate_search(browser, abstract, document)
    if verify_results_loaded(browser, abstract, document):
        count_results(browser, abstract, document)
        return handle_document_search(browser, abstract, document)
    else:
        return False
