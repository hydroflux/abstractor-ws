from selenium_utilities.inputs import click_button
from selenium_utilities.locators import locate_element_by_class_name

from settings.county_variables.jaguar import download_button_class
from settings.download_management import previously_downloaded, update_download
from actions.downloader import prepare_for_download


# Very similar but not identical to 'leopard' & 'tiger' execute_download
def execute_download(browser, abstract, document):
    click_button(browser, locate_element_by_class_name,  # Download Document
                 download_button_class, "download button", document)
    update_download(browser, abstract, document)


# Identical to 'leopard', 'tiger', 'rattlesnake', & 'eagle' download_document
def download_document(browser, abstract, document):
    prepare_for_download(abstract, document)
    if not previously_downloaded(abstract, document):
        execute_download(browser, abstract, document)
