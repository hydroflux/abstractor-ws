from selenium_utilities.locators import locate_element_by_name
from settings.iframe_handling import switch_to_default_content


def switch_to_main_frame(browser, abstract):
    switch_to_default_content(browser)
    main_frame = locate_element_by_name(browser, abstract.county.iframes['Main'], 'main iframe')
    browser.switch_to.frame(main_frame)


def switch_to_header_frame(browser, abstract):
    switch_to_main_frame(browser, abstract)
    header_frame = locate_element_by_name(browser, abstract.county.iframes['Header'], 'header iframe')
    browser.switch_to.frame(header_frame)


def switch_to_search_menu_frame(browser, abstract):
    switch_to_main_frame(browser, abstract)
    search_menu_frame = locate_element_by_name(browser, abstract.county.iframes['Search Menu'], 'search menu iframe')
    browser.switch_to.frame(search_menu_frame)


def switch_to_search_input_frame(browser, abstract):
    switch_to_search_menu_frame(browser, abstract)
    search_input_frame = locate_element_by_name(browser, abstract.county.iframes['Search Input'], 'search input iframe')
    browser.switch_to.frame(search_input_frame)


def switch_to_search_results_frame(browser, abstract):
    switch_to_main_frame(browser, abstract)
    result_frame = locate_element_by_name(browser, abstract.county.iframes['Search Results'], 'search results iframe')
    browser.switch_to.frame(result_frame)


def switch_to_search_results_list_frame(browser, abstract):
    switch_to_search_results_frame(browser, abstract)
    result_list_frame = locate_element_by_name(browser, abstract.county.iframes['Search Results List'],
                                               'search results list iframe')
    browser.switch_to.frame(result_list_frame)
