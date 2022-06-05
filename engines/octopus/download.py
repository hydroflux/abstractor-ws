from selenium_utilities.inputs import click_button
from selenium_utilities.locators import locate_element_by_id


def execute_download(browser, abstract, document):
    click_button(browser, locate_element_by_id, abstract.county.buttons["Download Prompt"],
                 "download prompt button", document)
    click_button(browser, locate_element_by_id, abstract.county.buttons["Download"],
                 "download button", document)
