from selenium_utilities.inputs import click_button
from selenium_utilities.locators import locate_element_by_id


# Very similar but not identical to 'jaguar' execute_download
def execute_download(browser, abstract, document):
    click_button(browser, locate_element_by_id, abstract.county.buttons["Download Submenu"],  # Open Download Submenu
                 "download submenu button", document)
    click_button(browser, locate_element_by_id, abstract.county.buttons["Download"],  # Execute Download
                 "execute download button", document)
