from engines.buffalo.frame_handling import switch_to_document_frame

from selenium_utilities.locators import locate_element


def get_next_result_button(browser, abstract, document):
    switch_to_document_frame(browser, abstract)
    return locate_element(browser, "id", abstract.county.buttons["Next Result"],
                          "next result button", True, document)


def next_result(browser, abstract, document):
    next_result_button = get_next_result_button(browser, abstract, document)
    # handle_click_next_result_button(browser, abstract, document, next_result_button)
    next_result_button.click()
