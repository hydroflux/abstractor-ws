import os

from selenium_utilities.inputs import click_button
from selenium_utilities.locators import locate_element_by_id

from settings.county_variables.leopard import (download_button_id,
                                               stock_download, view_group_id)
from settings.download_management import previously_downloaded, update_download
from settings.initialization import create_document_directory

# Use the following print statement to identify the best way to manage imports for Django vs the script folder
print("download", __name__)


# Very similar but not identical to 'jaguar' prepare_for_download
def prepare_for_download(abstract, document):
    abstract.document_directory = create_document_directory(abstract.target_directory)
    abstract.document_directory_files = len(os.listdir(abstract.document_directory))
    document.download_value = stock_download


# Very similar but not identical to 'jaguar' execute_download
def execute_download(browser, abstract, document):
    click_button(browser, locate_element_by_id, view_group_id, "download submenu", document)  # Open Download Submenu
    click_button(browser, locate_element_by_id, download_button_id, "download button", document)  # Download Document
    update_download(browser, abstract, document)


# Identical to 'jaguar' download_document
def download_document(browser, abstract, document):
    prepare_for_download(abstract, document)
    if not previously_downloaded(abstract, document):
        execute_download(browser, abstract, document)
