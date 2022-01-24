import os

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from settings.county_variables.leopard import (download_button_id,
                                               stock_download, view_group_id,
                                               view_panel_id)
from settings.download_management import previously_downloaded, update_download
from settings.file_management import (create_document_directory,
                                      extrapolate_document_value)
from settings.general_functions import timeout
from settings.invalid import no_document_image

# Use the following print statement to identify the best way to manage imports for Django vs the script folder
print("download", __name__)


def locate_download_submenu(browser, document):
    try:
        view_panel_present = EC.element_to_be_clickable((By.ID, view_panel_id))
        WebDriverWait(browser, timeout).until(view_panel_present)
        view_document_button = browser.find_element_by_id(view_group_id)
        return view_document_button
    except TimeoutException:
        print(f'Browser timed out trying to open document submenu for '
              f'{extrapolate_document_value(document)}.')


def open_download_submenu(browser, document):
    view_document_button = locate_download_submenu(browser, document)
    view_document_button.click()


def locate_download_button(browser, document):
    try:
        download_button_present = EC.element_to_be_clickable((By.ID, download_button_id))
        WebDriverWait(browser, timeout).until(download_button_present)
        download_button = browser.find_element_by_id(download_button_id)
        return download_button
    except TimeoutException:
        print(f'Browser timed out trying to click the download button for '
              f'{extrapolate_document_value(document)}.')


def execute_download(browser, document):
    download_button = locate_download_button(browser, document)
    download_button.click()


def download_document(browser, abstract, document):
    document_directory = create_document_directory(target_directory)
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
