import os

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium_utilities.inputs import click_button
from selenium_utilities.locators import locate_element_by_id

from settings.county_variables.leopard import (download_button_id,
                                               stock_download, view_group_id)
from settings.download_management import previously_downloaded, update_download
from settings.general_functions import timeout
from settings.initialization import create_document_directory
from settings.invalid import no_document_image

# Use the following print statement to identify the best way to manage imports for Django vs the script folder
print("download", __name__)


def open_download_submenu(browser, document):
    click_button(browser, locate_element_by_id, view_group_id, "download submenu",)


def execute_download(browser, document):
    click_button(browser, locate_element_by_id, download_button_id, "download button", document)


def download_document(browser, abstract, document):
    abstract.document_directory = create_document_directory(abstract.target_directory)
    if previously_downloaded(county, document_directory, document_number):
        return True
    else:
        number_files = len(os.listdir(document_directory))
        open_download_submenu(browser, document)
        execute_download(browser, document)
        if update_download(browser, county, stock_download, document_directory, number_files, document_number):
            return True
        else:
            no_document_image(abstract, document)
