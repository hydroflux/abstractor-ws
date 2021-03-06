from selenium_utilities.inputs import click_button
from selenium_utilities.locators import locate_element_by_class_name


# Very similar but not identical to 'leopard' & 'tiger' execute_download
def execute_download(browser, abstract, document):
    click_button(browser, locate_element_by_class_name,  # Download Document
                 abstract.county.buttons["Download"], "download button", document)
