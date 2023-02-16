from selenium_utilities.inputs import click_button
from selenium_utilities.locators import locate_element_by_id

from engines.dolphin.validation import check_for_document_image

# Exact same as "octopus" & "swordfish"


def execute_download(browser, abstract, document):
    click_button(browser, locate_element_by_id, abstract.county.buttons["Download Prompt"],
                 "download prompt button", document)
    if check_for_document_image(browser, abstract, document):
        click_button(browser, locate_element_by_id, abstract.county.buttons["Download"],
                     "download button", document)
    else:
        click_button(browser, locate_element_by_id, abstract.county.buttons["Cancel Download"],
                     "cancel download button", document)
