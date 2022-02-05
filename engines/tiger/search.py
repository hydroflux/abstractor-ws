from project_management.timers import naptime
from selenium_utilities.element_interaction import (center_element,
                                                    get_parent_element,
                                                    is_active_class)
from selenium_utilities.inputs import (clear_input, click_button,
                                       enter_input_value)
from selenium_utilities.locators import locate_element_by_id

from settings.general_functions import javascript_script_execution


def open_search(browser, abstract):
    # Messy => figure out a better way to do this
    javascript_script_execution(abstract.county.scripts["Search"])
    naptime()
    # This will probably not work great when called during the 'login' process
    ######
    search_navigation = locate_element_by_id(browser, abstract.county.ids["Search Navigation"], "search navigation", True)
    if is_active_class(search_navigation):
        return
    else:
        browser.execute_script(abstract.county.scripts["Search"])
        assert abstract.county.titles["Search"]


def open_search_tab(browser, abstract):
    search_tab = locate_element_by_id(browser, abstract.county.ids["Search Tab"], "search tab", True)
    center_element(browser, search_tab)
    if is_active_class(get_parent_element(search_tab)):
        return
    else:
        search_tab.click()


def clear_search(browser, abstract, document):
    clear_input(browser, locate_element_by_id, abstract.county.inputs["Reception Number"], "reception number input", document)


def handle_document_value_numbers(browser, abstract, document):
    value = document.value()
    if document.type == "document_number":
        enter_input_value(browser, locate_element_by_id, abstract.county.inputs["Reception Number"],
                          "reception number input", value, document)
    else:
        print(f'Unable to search document type "{document.type}", '
              f'a new search path needs to be developed in order to continue.\n')
        print("Please press enter after reviewing the search parameters...")
        input()


def execute_search(browser, abstract, document):
    handle_document_value_numbers(browser, abstract, document)
    click_button(browser, locate_element_by_id, abstract.county.buttons["Search"],
                 "execute search button", document)


def search(browser, abstract, document):
    open_search(browser, abstract)
    open_search_tab(browser, abstract)
    clear_search(browser, abstract, document)
    execute_search(browser, abstract, document)
