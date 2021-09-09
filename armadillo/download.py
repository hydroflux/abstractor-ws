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


def free_download(browser):
    pass


def add_to_cart(browser):
    pass


def download(browser):
    pass
