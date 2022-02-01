from selenium_utilities.inputs import click_button
from selenium_utilities.locators import locate_element_by_id

from settings.county_variables.leopard import (next_result_id,
                                               previous_result_id)
from settings.general_functions import scroll_to_top


def previous_result(browser, document):
    scroll_to_top(browser)
    click_button(browser, locate_element_by_id, previous_result_id, "previous result", document)


def next_result(browser, document):
    # next_result_button = get_next_result_button(browser, document)
    scroll_to_top(browser)  # should 'scroll_to_top' vs. 'center' be an option when clicking a button?
    click_button(browser, locate_element_by_id, next_result_id, "next result", document)
