import os

from selenium_utilities.inputs import click_button
from selenium_utilities.locators import locate_element_by_id

from settings.county_variables.leopard import (download_button_id,
                                               stock_download, view_group_id)
from settings.download_management import previously_downloaded, update_download
from settings.initialization import create_document_directory
from settings.invalid import no_document_image

# Use the following print statement to identify the best way to manage imports for Django vs the script folder
print("download", __name__)


def execute_download(browser, document):
    number_files = len(os.listdir(document_directory))
    click_button(browser, locate_element_by_id, view_group_id, "download submenu", document)  # Open Download Submenu
    click_button(browser, locate_element_by_id, download_button_id, "download button", document)  # Download Document


def download_document(browser, abstract, document):
    abstract.document_directory = create_document_directory(abstract.target_directory)
    if previously_downloaded(county, document_directory, document_number):
        return True
    else:
        execute_download(browser, document)
        if update_download(browser, county, stock_download, document_directory, number_files, document_number):
            return True
        else:
            no_document_image(abstract, document)
