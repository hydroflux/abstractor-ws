import os

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
    pass


def open_download_page():
    pass


def free_download():
    pass


def add_to_cart():
    pass


def execute_download():
    pass


def download_document():
    pass
