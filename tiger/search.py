from selenium_utilities.inputs import clear_input, click_button, enter_input_value

from selenium_utilities.locators import locate_element_by_id

from selenium_utilities.element_interaction import center_element, get_parent_element, is_active_class

if __name__ == '__main__':
    from settings.county_variables.tiger import (instrument_search_id,
                                                 search_button_id,
                                                 search_navigation_id,
                                                 search_script, search_tab_id,
                                                 search_title)
    from settings.settings import timeout
else:
    from ..settings.county_variables.tiger import (instrument_search_id,
                                                   search_button_id,
                                                   search_navigation_id,
                                                   search_script,
                                                   search_tab_id, search_title)
    from ..settings.settings import timeout


def open_search(browser):
    search_navigation = locate_element_by_id(browser, search_navigation_id, "search navigation", True)
    if is_active_class(search_navigation):
        return
    else:
        browser.execute_script(search_script)
        assert search_title


def open_search_tab(browser):
    search_tab = locate_element_by_id(browser, search_tab_id, "search tab", True)
    center_element(browser, search_tab)
    if is_active_class(get_parent_element(search_tab)):
        return
    else:
        search_tab.click()


def clear_search(browser, document):
    clear_input(browser, locate_element_by_id, instrument_search_id, "reception number input", document)


def handle_document_value_numbers(browser, document):
    value = document.value()
    if document.type == "document_number":
        enter_input_value(browser, locate_element_by_id, instrument_search_id,
                          "reception number input", value, document)
    else:
        print(f'Unable to search document type "{document.type}", '
              f'a new search path needs to be developed in order to continue.\n')
        print("Please press enter after reviewing the search parameters...")
        input()


def execute_search(browser, document):
    handle_document_value_numbers(browser, document)
    click_button(browser, locate_element_by_id, search_button_id,
                 "execute search button", document)


def search(browser, document):
    open_search(browser)
    open_search_tab(browser)
    clear_search(browser, document)
    execute_search(browser, document)
