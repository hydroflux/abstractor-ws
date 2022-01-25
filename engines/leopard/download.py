import os

from selenium_utilities.inputs import click_button
from selenium_utilities.locators import locate_element_by_id

from settings.county_variables.leopard import (download_button_id,
                                               stock_download, view_group_id)
from settings.download_management import previously_downloaded, update_download
from settings.file_management import document_downloaded
from settings.initialization import create_document_directory
from settings.invalid import no_download

# Use the following print statement to identify the best way to manage imports for Django vs the script folder
print("download", __name__)


# Very similar but not identical to 'jaguar' execute_download
def execute_download(browser, abstract, document):
    document.download_value = stock_download
    number_files = len(os.listdir(abstract.document_directory))
    click_button(browser, locate_element_by_id, view_group_id, "download submenu", document)  # Open Download Submenu
    click_button(browser, locate_element_by_id, download_button_id, "download button", document)  # Download Document
    if update_download(
        browser,
        abstract.document_directory,
        document,
        number_files
    ):
        document_downloaded(abstract.document_list, document)
    else:
        no_download(abstract, document)


# Identical to 'jaguar' download_document
def download_document(browser, abstract, document):
    abstract.document_directory = create_document_directory(abstract.target_directory)
    if previously_downloaded(abstract, document):
        document_downloaded(abstract.document_list, document)
        return True
    else:
        execute_download(browser, abstract, document)
