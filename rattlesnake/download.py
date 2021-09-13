import os
from rattlesnake.validation import verify_document_image_page_loaded

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from settings.download_management import previously_downloaded, update_download
from settings.file_management import (create_document_directory,
                                      extrapolate_document_value)
from settings.general_functions import (center_element, get_direct_link,
                                        newline_split, timeout)

from rattlesnake.rattlesnake_variables import download_page_id, free_download_id, add_to_cart_id


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


def free_download():
    pass


def add_to_cart():
    pass


def execute_download():
    pass


def download_document(browser, document):
    open_download_page(browser, document)
    verify_document_image_page_loaded(browser, document)
