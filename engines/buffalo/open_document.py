from project_management.timers import naptime
from settings.general_functions import eight_character_padding, four_character_padding

from engines.buffalo.frame_handling import switch_to_search_result_list_frame
from engines.buffalo.validation import page_is_loaded

from selenium_utilities.locators import locate_element


def get_result_links(browser, abstract, document):
    link_elements = locate_element(browser, "classes", abstract.county.classes["Result Link"], "result links",
                                   True, document, alternate=abstract.county.classes["Visited Result Link"])
    while link_elements is None:
        link_elements = locate_element(browser, "classes", abstract.county.classes["Result Link"], "result links",
                                       True, document, alternate=abstract.county.classes["Visited Result Link"])
    return link_elements


def count_results(browser, abstract, document):
    switch_to_search_result_list_frame(browser, abstract)
    result_links = get_result_links(browser, abstract, document)
    document.number_results += int(len(result_links)/2)
    if document.number_results > 1:
        print(f'{document.number_results} documents returned while searching '
              f'{document.extrapolate_value()}.')


def get_first_result_link(browser, abstract, document):
    switch_to_search_result_list_frame(browser, abstract)
    return locate_element(browser, "id", abstract.county.ids["First Result Link"],
                          "first result", True, document)


def get_first_result(browser, abstract, document):
    if document.type == "document_number":
        return get_first_result_link(browser, abstract, document)
    elif document.type == "book_and_page":
        switch_to_search_result_list_frame(browser, abstract)
        return locate_element(browser, "xpath", abstract.county.ids["Book And Page First Result"],
                              "first result", True, document)


def verify_first_document_search_result(browser, abstract, document):
    first_result = get_first_result(browser, abstract, document).text
    if document.type == "document_number":
        if first_result == eight_character_padding(document.value):
            return True
    elif document.type == "book_and_page":
        book, page = document.document_value()
        if first_result == f'{four_character_padding(book)} {four_character_padding(page)}':
            return True


def process_open_document(browser, abstract, document):
    if verify_first_document_search_result(browser, abstract, document):
        get_first_result_link(browser, abstract, document).click()
    else:
        print(f'First search result located does not match the searched document '
              f'{document.extrapolate_value()}, please review')
        input()


def open_document(browser, abstract, document):
    naptime()
    if page_is_loaded(browser, abstract, abstract.county.messages["Search Results"], document):
        count_results(browser, abstract, document)
        process_open_document(browser, abstract, document)
        return True
