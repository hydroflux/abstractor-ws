from engines.rabbit.error_handling import check_for_browser_error

from project_management.timers import naptime

from selenium_utilities.element_interaction import get_parent_element, is_active_class
from selenium_utilities.inputs import clear_input, click_button, enter_input_value
from selenium_utilities.locators import locate_element_by_id
from selenium_utilities.open import open_url


# def access_search_navigation_tab(browser, abstract, document):
#     search_navigation_tab = locate_element_by_id(browser, abstract.county.ids["Search Navigation"],
#                                                  "search navigation", True, document)
#     while search_navigation_tab is None:
#         search_navigation_tab = locate_element_by_id(browser, abstract.county.ids["Search Navigation"],
#                                                      "search navigation", True, document)
#     search_navigation_tab.click()
#     return search_navigation_tab


def open_search(browser, abstract, document):
    if document.type == "document_number":
        open_url(browser, abstract.county.urls['Document Search'],
                 abstract.county.titles['Document Search'], 'search page', document)
    elif document.type == "name":
        open_url(browser, abstract.county.urls['Name Search'],
                 abstract.county.titles['Name Search'], 'document search page', document)
    # navigation_tab = access_search_navigation_tab(browser, abstract, document)
    # print("navigation tab", navigation_tab)
    # print("")
    # while not is_active_class(navigation_tab):
    #     print("Navigation tab not active, attempting to connect again.")
    #     naptime()  # Allows time for navigation to load
    #     navigation_tab = access_search_navigation_tab(browser, abstract, document)


def access_search_type_tab(browser, document, attribute, type):
    search_type_tab = get_parent_element(locate_element_by_id(browser, attribute, type, True, document))
    while search_type_tab is None:
        check_for_browser_error(browser)
        search_type_tab = get_parent_element(locate_element_by_id(browser, attribute, type, True, document))
    return search_type_tab


def open_tab(browser, document, attribute, type):
    tab = access_search_type_tab(browser, document, attribute, type)
    while not is_active_class(tab):
        tab = access_search_type_tab(browser, document, attribute, type)
        tab.click()


def open_search_type_tab(browser, abstract, document):
    if document.type == "document_number":
        open_tab(browser, document, abstract.county.ids["Document Search Tab"], "document search tab")
    elif document.type == "name":
        open_tab(browser, document, abstract.county.ids["Name Search Tab"], "name search tab")
    else:
        print(f'Abstractor path has not yet been developed to "open_search_type_tab" for document type "\
               {document.type}", please review...')
        input()


def clear_search(browser, abstract, document):
    if document.type == "document_number":
        clear_input(browser, locate_element_by_id, abstract.county.inputs["Reception Number"],
                    "document search field", document)
    elif document.type == "name":
        clear_input(browser, locate_element_by_id, abstract.county.inputs["Name"],
                    "name search field", document)
        clear_input(browser, locate_element_by_id, abstract.county.inputs["Start Date"],
                    "name search start date field", document)
        clear_input(browser, locate_element_by_id, abstract.county.inputs["End Date"],
                    "name search end date field", document)
    else:
        print(f'Abstractor path has not yet been developed to "clear_search" for document type "\
               {document.type}", please review...')
        input()


def handle_document_value_numbers(browser, abstract, document):
    if document.type == "document_number":
        enter_input_value(browser, locate_element_by_id, abstract.county.inputs["Reception Number"],
                          "document search field", document.document_value())
    elif document.type == "name":
        enter_input_value(browser, locate_element_by_id, abstract.county.inputs["Name"],
                          "name search field", document.document_value())
        enter_input_value(browser, locate_element_by_id, abstract.county.inputs["Start Date"],
                          "name search start field", document.document_value())
        enter_input_value(browser, locate_element_by_id, abstract.county.inputs["End Date"],
                          "name search end date field", document.document_value())
    else:
        print(f'Abstractor path has not yet been developed to "handle_document_value_numbers" for document type "\
               {document.type}", please review...')
        input()


def execute_search(browser, abstract, document):
    if document.type == "document_number":
        click_button(browser, locate_element_by_id, abstract.county.buttons["Document Search"],
                     "document search button", document)
    elif document.type == "name":
        click_button(browser, locate_element_by_id, abstract.county.buttons["Name Search"],
                    "name search button", document)
    else:
        print(f'Abstractor path has not yet been developed to "execute_search" for document type "\
               {document.type}", please review...')
        input()


def search(browser, abstract, document):
    open_search(browser, abstract, document)
    open_search_type_tab(browser, abstract, document)
    clear_search(browser, abstract, document)
    handle_document_value_numbers(browser, abstract, document)
    execute_search(browser, abstract, document)
