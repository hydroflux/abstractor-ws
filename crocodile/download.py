import os

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from settings.download_management import previously_downloaded, update_download
from settings.file_management import (create_document_directory,
                                      extrapolate_document_value)
from settings.general_functions import javascript_script_execution, timeout

from crocodile.crocodile_variables import download_menu_id, download_button_tag


def open_document_download_page(browser, document):
    javascript_script_execution(browser, document.link)


def locate_download_menu(browser, document):
    try:
        download_menu_present = EC.presence_of_element_located((By.ID, download_menu_id))
        WebDriverWait(browser, timeout).until(download_menu_present)
        download_menu = browser.find_element_by_id(download_menu_id)
        return download_menu
    except TimeoutException:
        print(f'Browser timed out trying to locate download menu for '
              f'{extrapolate_document_value(document)}, please review.')


def locate_download_button(download_menu, document):
    try:
        download_button_present = EC.element_to_be_clickable((By.TAG_NAME, download_button_tag))
        WebDriverWait(download_menu, timeout).until(download_button_present)
        download_button = download_menu.find_element_by_tag_name(download_button_tag)
        return download_button
    except TimeoutException:
        print(f'Browser timed out trying to locate download button for '
              f'{extrapolate_document_value(document)}, please review.')


def get_download_button(browser, document):
    download_menu = locate_download_menu(browser, document)
    return locate_download_button(download_menu, document)


def locate_download_confirmation_button():
    pass


def confirm_document_download():
    pass


def execute_download(browser, document):
    download_button = get_download_button(browser, document)
    download_button.click()


def download_document(browser, county, target_directory, document):
    document_directory = create_document_directory(target_directory)
    if previously_downloaded(county, document_directory, document.reception_number):
        return True
    else:
        number_files = len(os.listdir(document_directory))
        open_document_download_page(browser, document)
    pass
