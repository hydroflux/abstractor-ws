import os

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from settings.download_management import previously_downloaded, update_download
from settings.file_management import (create_document_directory,
                                      extrapolate_document_value)
from settings.general_functions import assert_window_title, javascript_script_execution, timeout

from crocodile.crocodile_variables import (document_image_title,
                                           download_button_tag,
                                           download_confirmation_id,
                                           download_confirmation_title,
                                           download_menu_id, stock_download)


def open_document_download_page(browser, document):
    javascript_script_execution(browser, document.link)
    if not assert_window_title(browser, document_image_title):
        print(f'Browser failed to open document download page for '
              f'{extrapolate_document_value(document)}, please review.')


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


def open_document_submenu(browser, document):
    download_button = get_download_button(browser, document)
    download_button.click()


def locate_download_confirmation_button(browser, document):
    try:
        download_confirmation_present = EC.element_to_be_clickable((By.ID, download_confirmation_id))
        WebDriverWait(browser, timeout).until(download_confirmation_present)
        download_confirmation_button = browser.find_element_by_id(download_confirmation_id)
        return download_confirmation_button
    except TimeoutException:
        print(f'Browser timed out trying to locate download confirmation button for '
              f'{extrapolate_document_value(document)}, please review.')


def confirm_document_download(browser, document):
    download_confirmation_button = locate_download_confirmation_button(browser, document)
    download_confirmation_button.click()


def execute_download(browser, document):
    open_document_download_page(browser, document)
    open_document_submenu(browser, document)
    confirm_document_download(browser, document)


def close_download_window(browser, document):
    windows = browser.window_handles
    if len(windows) > 1:
        browser.switch_to.window(windows[1])
        if assert_window_title(browser, download_confirmation_title):
            browser.close()
            browser.switch_to_window(windows[0])
        else:
            print(f'Browser failed to close download window after downloading '
                  f'{extrapolate_document_value(document)}, please review.')


def download_document(browser, county, target_directory, document):
    document_directory = create_document_directory(target_directory)
    reception_number = document.reception_number
    if previously_downloaded(county, document_directory, reception_number):
        return True
    else:
        number_files = len(os.listdir(document_directory))
        execute_download(browser, document)
        if update_download(browser, county, stock_download, document_directory, number_files, reception_number):
            close_download_window(browser, document)
            return True
