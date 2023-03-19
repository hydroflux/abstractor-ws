from selenium.common.exceptions import StaleElementReferenceException

from project_management.timers import naptime
from selenium_utilities.locators import locate_element
from serializers.validator import check_for_alert
from settings.invalid import no_document_image

from engines.buffalo.frame_handling import (switch_to_captcha_frame,
                                            switch_to_document_image_frame,
                                            switch_to_header_frame,
                                            switch_to_search_menu_frame)


def check_header_validation(browser, abstract, validation_text):
    try:
        switch_to_header_frame(browser, abstract)
        header_text_element = locate_element(browser, "tag", abstract.county.tags["Header Text"],
                                             "header text")
        return header_text_element.text.startswith(validation_text)
    except StaleElementReferenceException:
        print("Encountered a stale element reference exception, trying again.")


def header_validation(browser, abstract, validation_text):
    validated = check_header_validation(browser, abstract, validation_text)
    while validated is None:
        validated = check_header_validation(browser, abstract, validation_text)
    if validated:
        return validated
    else:
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


def check_for_captcha(browser, abstract, document):
    # Loop through a couple times with pauses to see if the captcha is hit early on?
    # start with prints and then switch to input?
    while switch_to_captcha_frame(browser, abstract):
        input(f'Encountered a captcha while processing abstract for document {document.extrapolate_value()}, '
              f'please address and press enter to continue...')


def check_for_document_image(browser, abstract, document):
    switch_to_document_image_frame(browser, abstract)
    no_document_image_element = locate_element(browser, "id", abstract.county.ids["No Document Image"],
                                               "no document image", False, document, True)
    if no_document_image_element is not None:
        if no_document_image_element.text.strip() == abstract.county.messages["No Document Image"]:
            no_document_image(abstract, document)
        else:
            input("Encountered an unknown document image error, please review and press enter to continue...")


def check_for_download_alert(browser, abstract, document):
    if check_for_alert(browser, abstract.county.messages["No Document Image Alert"]):
        no_document_image(abstract, document)


def page_is_loaded(browser, abstract, validation_text, document=None):
    check_for_captcha(browser, abstract, document)
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
        return True
