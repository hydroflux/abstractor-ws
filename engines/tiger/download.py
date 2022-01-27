import os

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium_utilities.inputs import click_button
from selenium_utilities.locators import locate_element_by_id

from settings.county_variables.tiger import (download_button_id,
                                             stock_download, view_group_id,
                                             view_panel_id)
from settings.download_management import update_download
from settings.file_management import create_document_directory
from settings.general_functions import timeout

# Use the following print statement to identify the best way to manage imports for Django vs the script folder
print("download", __name__)


# Very similar but not identical to 'jaguar' prepare_for_download
# Identical to the 'leopard' prepare_for_download
def prepare_for_download(abstract):
    abstract.document_directory = create_document_directory(abstract.target_directory)
    abstract.document_directory_files = len(os.listdir(abstract.document_directory))


def execute_download(browser, document_number):
    try:
        download_button_present = EC.element_to_be_clickable((By.ID, download_button_id))
        WebDriverWait(browser, timeout).until(download_button_present)
        download_button = browser.find_element_by_id(download_button_id)
        download_button.click()
    except TimeoutException:
        print(f'Browser timed out trying to click the download button for document number {document_number}.')


def download_document(browser, abstract, document):
    prepare_for_download(abstract)
    click_button(browser, locate_element_by_id, view_panel_id, "download submenu", document)  # Open Document Submenu
    execute_download(browser, document_number)
    if update_download(browser, county, stock_download, document_directory, document_number):
        return True
