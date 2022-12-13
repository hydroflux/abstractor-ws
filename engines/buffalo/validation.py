from engines.buffalo.frame_handling import (switch_to_captcha_frame,
                                            switch_to_header_frame,
                                            switch_to_search_menu_frame)
from project_management.timers import naptime

from selenium_utilities.locators import locate_element


def check_header_validation(browser, abstract, validation_text):
    switch_to_header_frame(browser, abstract)
    header_text_element = locate_element(browser, "tag", abstract.county.tags["Header Text"],
                                         "header text")
    return header_text_element.text.startswith(validation_text)


def header_validation(browser, abstract, validation_text):
    validated = check_header_validation(browser, abstract, validation_text)
    if validated:
        return validated
    else:
        print("SECOND PAGE VALIDATION CHECK")
        # Performs a second check for cases where page load is delayed
        naptime()
        return check_header_validation(browser, abstract, validation_text)


# BUILD THIS OUT
# def double_check(browser, abstract, validation_text, validation_function):
#     validated = validation_function(browser, abstract, validation_text)
#     if validated:
#         return validated
#     else:
#         print(f'SECOND PAGE VALIDATION CHECK "{validation_text}"')
#         # Performs a second check for cases where page load is delayed
#         naptime()
#         return validation_function(browser, abstract, validation_text)

def check_for_document_results(browser, abstract, document):
    switch_to_search_menu_frame(browser, abstract)
    no_results_message_element = locate_element(browser, "id", abstract.county.ids["No Results"],
                                                "no results message", document=document)
    no_results_message = no_results_message_element.text.strip()
    return no_results_message != abstract.county.messages["No Results"]


def check_for_captcha(browser, abstract):
    # Loop through a couple times with pauses to see if the captcha is hit early on?
    # start with prints and then switch to input?
    while switch_to_captcha_frame(browser, abstract):
        input("Encountered a captcha while processing abstract, please address and press enter to continue...")


def page_is_loaded(browser, abstract, validation_text, document=None):
    if not header_validation(browser, abstract, validation_text):
        if validation_text == abstract.county.messages["Search Results"]:
            if check_for_document_results(browser, abstract, document):
                print(f'Browser indicates that it has not properly loaded '
                      f'"{validation_text}", please review webdriver before continuing...')
                input()
        else:
            print(f'Browser indicates that it has not properly loaded '
                  f'"{validation_text}", please review webdriver before continuing...')
            input()
    else:
        check_for_captcha(browser, abstract)
        return True
