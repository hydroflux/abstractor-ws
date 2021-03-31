import os
from time import sleep, time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from .variables import view_panel_id, view_group_id, download_button_id, stock_download, timeout


def open_document_submenu(browser, document_number):
    try:
        view_panel_present = EC.element_to_be_clickable((By.ID, view_panel_id))
        WebDriverWait(browser, timeout).until(view_panel_present)
        view_document = browser.find_element_by_id(view_group_id)
        view_document.click()
    except TimeoutException:
        print(f'Browser timed out trying to open document submenu for document number {document_number}.')


def execute_download(browser, document_number):
    try:
        download_button_present = EC.element_to_be_clickable((By.ID, download_button_id))
        WebDriverWait(browser, timeout).until(download_button_present)
        download_button = browser.find_element_by_id(download_button_id)
        download_button.click()
    except TimeoutException:
        print(f'Browser timed out trying to click the download button for document number {document_number}.')


def check_for_download_error(browser):
    handles = browser.window_handles
    number_windows = len(handles)
    if number_windows > 1:
        window_before_click = handles[0]
        window_after_click = handles[1]
        browser.switch_to_window(window_after_click)
        if browser.title == 'Error':
            browser.close()
            browser.switch_to_window(window_before_click)
            return True
        else:
            browser.switch_to_window(window_before_click)


def wait_for_download(browser, download_path):
    check_for_error = time() + 10
    while not os.path.exists(download_path):
        sleep(0.5)
        if time() > check_for_error:
            check_for_download_error(browser)


def check_download_size(new_download_name, document_number):
    size = os.state(new_download_name) == 0
    if size:
        os.remove(new_download_name)
        print(f'Failed to download document number {document_number}.')


def rename_download(document_directory, document_number, download_path, new_download_name):
    if os.path.isfile(download_path):
        os.rename(stock_download, new_download_name)
        os.chdir(document_directory)
        check_download_size(document_number, new_download_name)
    else:
        raise ValueError("%s isn't a file!" % download_path)


def update_download(browser, county, document_directory, document_number):
    download_path = f'{document_directory}/{stock_download}'
    if wait_for_download(browser, download_path):
        return False
    else:
        new_download_name = f'{county.prefix}-{document_number}.pdf'
        rename_download(document_directory, document_number, download_path, new_download_name)


def download_document(browser, county, document_directory, document_number):
    open_document_submenu(browser, document_number)
    execute_download(browser, document_number)
    if update_download(county, document_directory, document_number):
        return True
