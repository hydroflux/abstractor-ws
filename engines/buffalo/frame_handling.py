from selenium_utilities.locators import locate_element_by_name
from settings.iframe_handling import switch_to_default_content


def switch_to_main_frame(browser, abstract):
    switch_to_default_content(browser)
    main_frame = locate_element_by_name(browser, abstract.county.iframes["Main"],
                                        "main iframe")
    browser.switch_to.frame(main_frame)


def switch_to_header_frame(browser, abstract):
    switch_to_main_frame(browser, abstract)
    header_frame = locate_element_by_name(browser, abstract.county.iframes["Header"],
                                          "header iframe")
    browser.switch_to.frame(header_frame)


def switch_to_search_menu_frame(browser, abstract):
    switch_to_main_frame(browser, abstract)
    search_menu_frame = locate_element_by_name(browser, abstract.county.iframes["Search Menu"],
                                               "search menu iframe")
    browser.switch_to.frame(search_menu_frame)


def switch_to_search_input_frame(browser, abstract):
    switch_to_search_menu_frame(browser, abstract)
    search_input_frame = locate_element_by_name(browser, abstract.county.iframes["Search Input"],
                                                "search input iframe")
    browser.switch_to.frame(search_input_frame)


def switch_to_search_result_frame(browser, abstract):
    switch_to_main_frame(browser, abstract)
    result_frame = locate_element_by_name(browser, abstract.county.iframes["Result"],
                                          "result iframe")
    browser.switch_to.frame(result_frame)


def switch_to_search_result_list_frame(browser, abstract):
    switch_to_search_result_frame(browser, abstract)
    result_list_frame = locate_element_by_name(browser, abstract.county.iframes["Result List"],
                                               "result list iframe")
    browser.switch_to.frame(result_list_frame)


def switch_to_document_frame(browser, abstract):
    switch_to_main_frame(browser, abstract)
    document_frame = locate_element_by_name(browser, abstract.county.iframes["Document"],
                                            "document iframe")
    browser.switch_to.frame(document_frame)


def switch_to_document_information_frame(browser, abstract):
    switch_to_document_frame(browser, abstract)
    document_information_frame = locate_element_by_name(browser, abstract.county.iframes["Document Information"],
                                                        "document information iframe")
    browser.switch_to.frame(document_information_frame)


def switch_to_related_documents_menu_frame(browser, abstract):
    switch_to_document_information_frame(browser, abstract)
    related_documents_menu_frame = locate_element_by_name(browser, abstract.county.iframes["Related Documents Menu"],
                                                          "related documents menu iframe")
    browser.switch_to.frame(related_documents_menu_frame)


def switch_to_document_image_frame(browser, abstract):
    switch_to_document_frame(browser, abstract)
    document_image_frame = locate_element_by_name(browser, abstract.county.iframes["Document Image"],
                                                  "document image iframe")
    browser.switch_to.frame(document_image_frame)


def switch_to_download_submenu_frame(browser, abstract):
    switch_to_main_frame(browser, abstract)
    download_submenu_frame = locate_element_by_name(browser, abstract.county.iframes["Download Submenu"],
                                                    "download submenu iframe")
    browser.switch_to.frame(download_submenu_frame)


def switch_to_download_frame(browser, abstract):
    switch_to_default_content(browser)
    download_frame = locate_element_by_name(browser, abstract.county.iframes["Download"],
                                            "download iframe")
    browser.switch_to.frame(download_frame)


def switch_to_captcha_frame(browser, abstract):
    switch_to_search_result_frame(browser, abstract)
    captcha_frame = locate_element_by_name(browser, abstract.county.iframes["Captcha"],
                                           "captcha iframe", quick=True)
    if captcha_frame is not None:
        browser.switch_to.frame(captcha_frame)
        return True
