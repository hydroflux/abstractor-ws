import os

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from settings.download_management import previously_downloaded, update_download
from settings.file_management import create_document_directory
from settings.general_functions import long_timeout, naptime
# from settings.error_handling import no_image_comment

from armadillo.armadillo_variables import download_page_class_name


def build_stock_download(document):
    pass


def free_download(browser):
    pass


def add_to_cart(browser, document):
    pass


def execute_download(browser, document_directory, document, download_type):
    if download_type == 'free':
        return free_download(browser, document_directory, document)
    elif download_type == 'paid':
        return add_to_cart(browser, document)


def download(browser, county, target_directory, document, download_type):
    document_directory = create_document_directory(target_directory)
    if previously_downloaded(county, document_directory, document.reception_number):
        return True
    else:
        return execute_download(browser, document_directory, document, download_type)
