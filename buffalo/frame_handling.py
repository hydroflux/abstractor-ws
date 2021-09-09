from settings.iframe_handling import locate_iframe_by_name, switch_to_default_content

from buffalo.buffalo_variables import (header_frame_name, main_frame_name,
                                       result_frame_name,
                                       result_list_frame_name,
                                       search_input_frame_name,
                                       search_menu_frame_name)


def switch_to_main_frame(browser):
    switch_to_default_content(browser)
    main_frame = locate_iframe_by_name(browser, main_frame_name)
    browser.switch_to.frame(main_frame)


def switch_to_header_frame(browser):
    switch_to_main_frame(browser)
    header_frame = locate_iframe_by_name(browser, header_frame_name)
    browser.switch_to.frame(header_frame)


def switch_to_search_menu_frame(browser):
    switch_to_main_frame(browser)
    search_menu_frame = locate_iframe_by_name(browser, search_menu_frame_name)
    browser.switch_to.frame(search_menu_frame)


def switch_to_search_input_frame(browser):
    switch_to_search_menu_frame(browser)
    search_input_frame = locate_iframe_by_name(browser, search_input_frame_name)
    browser.switch_to.frame(search_input_frame)


def switch_to_search_result_frame(browser):
    switch_to_main_frame(browser)
    result_frame = locate_iframe_by_name(browser, result_frame_name)
    browser.switch_to_frame(result_frame)


def switch_to_search_result_list_frame(browser):
    switch_to_search_result_frame(browser)
    result_list_frame = locate_iframe_by_name(browser, result_list_frame_name)
    browser.switch_to_frame(result_list_frame)
