from project_management.timers import naptime
from settings.general_functions import eight_character_padding

from engines.buffalo.frame_handling import switch_to_search_result_list_frame
from engines.buffalo.validation import page_is_loaded

from selenium_utilities.locators import locate_element


def get_result_links(browser, abstract, document):
    link_elements = locate_element(browser, "classes", abstract.county.classes["Result Link"],
                                   "result links", True, document)
    while link_elements is None:
        link_elements = locate_element(browser, "classes", abstract.county.classes["Result Link"],
                                       "result links", True, document)
    return link_elements


def count_results(browser, abstract, document):
    switch_to_search_result_list_frame(browser, abstract)
    result_links = get_result_links(browser, abstract, document)
    document.number_results += len(result_links[:-1])


def check_search_results(browser, abstract, document):
    count_results(browser, abstract, document)
    if document.number_results > 1:
        input(f'Returned {document.number_results} results while searching for '
              f'{document.extrapolate_value()}... Please review application logic for processing '
              f'{document.number_results} results.')
    else:
        return True


def get_first_result(browser, abstract, document):
    switch_to_search_result_list_frame(browser, abstract)
    return locate_element(browser, "id", abstract.county.ids["First Result"],
                          "first result", True, document)


def verify_first_document_search_result(browser, abstract, document):
    first_result = get_first_result(browser, abstract, document).text
    if first_result == eight_character_padding(document.value):
        return True


def open_document_number(browser, abstract, document):
    if verify_first_document_search_result(browser, abstract, document):
        get_first_result(browser, abstract, document).click()
    else:
        print(f'First search result located does not match the searched document '
              f'{document.extrapolate_value()}, please review')
        input()


def process_open_document(browser, abstract, document):
    if document.type == "document_number":
        open_document_number(browser, abstract, document)
    else:
        print(f'Document type {document.type} not currently available, '
              f'please review entry...')
        input()


def open_document(browser, abstract, document):
    naptime()
    if page_is_loaded(browser, abstract, abstract.county.messages["Search Results"], document):
        if check_search_results(browser, abstract, document):
            process_open_document(browser, abstract, document)
            return True
