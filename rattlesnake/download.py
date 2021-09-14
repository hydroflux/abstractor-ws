import os

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from settings.download_management import previously_downloaded, update_download
from settings.file_management import (create_document_directory,
                                      extrapolate_document_value)
from settings.general_functions import timeout

from rattlesnake.rattlesnake_variables import (add_to_cart_button_id,
                                               download_page_id,
                                               free_download_button_id)
from rattlesnake.validation import verify_document_image_page_loaded


def locate_download_page(browser, document):
    try:
        download_page_present = EC.presence_of_element_located((By.ID, download_page_id))
        WebDriverWait(browser, timeout).until(download_page_present)
        download_page = browser.find_element_by_id(download_page_id)
        return download_page
    except TimeoutException:
        print(f'Browser timed out trying to locate download page for '
              f'{extrapolate_document_value(document)}, please review.')
        input()


def open_download_page(browser, document):
    download_page = locate_download_page(browser, document)
    download_page.click()


def locate_button(browser, document, id, button_type):
    try:
        button_present = EC.element_to_be_clickable((By.ID, id))
        WebDriverWait(browser, timeout).until(button_present)
        button = browser.find_element_by_id(id)
        return button
    except TimeoutException:
        print(f'Browser timed out trying to locate "{button_type}" button for '
              f'{extrapolate_document_value(document)}, please review.')
        input()


def free_download(browser, document):
    free_download_button = locate_button(browser, document, free_download_button_id, 'free download')
    free_download_button.click()


def add_to_cart(browser, document):
    add_to_cart_button = locate_button(browser, document, add_to_cart_button_id, 'free download')
    add_to_cart_button.click()


def execute_download(browser, county, document_directory, document):
    if document.download_type == 'free':
        free_download(browser, document)
        return update_download(
            browser,
            county,
            '',
            document_directory,
            len(os.listdir(document_directory)),
            document.reception_number,
            'alt'
            )
    elif document.download_type == 'paid':
        return add_to_cart(browser, document)


def download_document(browser, county, target_directory, document):
    document_directory = create_document_directory(target_directory)
    if previously_downloaded(county, document_directory, document.value):
        return True
    else:
        open_download_page(browser, document)
        if verify_document_image_page_loaded(browser, document):
            return execute_download(browser, county, document_directory, document)
