from selenium_utilities.inputs import click_button, enter_input_value, enter_datepicker_value
from selenium_utilities.locators import locate_element_by_class_name, locate_element_by_css_selector
from selenium_utilities.open import open_url


def perform_name_search(browser, abstract):
    enter_input_value(browser, locate_element_by_css_selector, abstract.county.inputs["Search Input"],
                      "search value input", abstract.search_name, document=None)
    enter_datepicker_value(browser, locate_element_by_css_selector, abstract.county.inputs["Start Date"],
                      "search start date input", abstract.start_date, document=None)
    enter_datepicker_value(browser, locate_element_by_css_selector, abstract.county.inputs["End Date"],
                      "search end date input", abstract.end_date, document=None)
    click_button(browser, locate_element_by_class_name, abstract.county.buttons["Search"],
                 "execute search button", document=None)


def search(browser, abstract, document=None):
    if abstract.program == "name_search":
        if not abstract.number_search_results:
            perform_name_search(browser, abstract)
    else:
        open_url(browser, abstract.county.urls["Search Page"],
                abstract.county.titles["Search Page"], "search page")
        value = document.document_value()
        enter_input_value(browser, locate_element_by_css_selector, abstract.county.inputs["Search Input"],
                        "search value input", value, document)
        click_button(browser, locate_element_by_class_name, abstract.county.buttons["Search"],
                    "execute search button", document)
