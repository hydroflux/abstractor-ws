from engines.buffalo.frame_handling import switch_to_header_frame

from selenium_utilities.locators import locate_element_by_tag_name


def header_validation(browser, abstract, validation_text):
    switch_to_header_frame(browser, abstract)
    header_text_element = locate_element_by_tag_name(browser, abstract.county.tags["Header Text"],
                                                     "header text")
    return header_text_element.text.startswith(validation_text)


def page_is_loaded(browser, abstract, validation_text):
    if not header_validation(browser, abstract, validation_text):
        print(f'Browser indicates that it has not properly loaded '
              f'"{validation_text}", please review webdriver before continuing...')
        input()
    else:
        return True
