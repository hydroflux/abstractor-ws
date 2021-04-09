from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from settings.download_management import update_download
from settings.file_management import create_document_directory, extrapolate_document_value
from settings.settings import timeout

from leopard.leopard_variables import (download_button_id, stock_download,
                                       view_group_id, view_panel_id)

# Use the following print statement to identify the best way to manage imports for Django vs the script folder
print("download", __name__)

def open_document_submenu(browser, document):
    try:
        view_panel_present = EC.element_to_be_clickable((By.ID, view_panel_id))
        WebDriverWait(browser, timeout).until(view_panel_present)
        view_document = browser.find_element_by_id(view_group_id)
        view_document.click()
    except TimeoutException:
        print(f'Browser timed out trying to open document submenu for '
              f'{extrapolate_document_value(document)}.')


def execute_download(browser, document):
    try:
        download_button_present = EC.element_to_be_clickable((By.ID, download_button_id))
        WebDriverWait(browser, timeout).until(download_button_present)
        download_button = browser.find_element_by_id(download_button_id)
        download_button.click()
    except TimeoutException:
        print(f'Browser timed out trying to click the download button for '
              f'{extrapolate_document_value(document)}.')


def download_document(browser, county, target_directory, document, document_number):
    document_directory = create_document_directory(target_directory)
    open_document_submenu(browser, document)
    execute_download(browser, document)
    if update_download(browser, county, stock_download, document_directory, document_number):
        return True
