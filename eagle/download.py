from time import sleep

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from settings.download_management import update_download
from settings.file_management import create_document_directory

# Use the following print statement to identify the best way to manage imports for Django vs the script folder
print("download", __name__)

from settings.settings import long_timeout

from eagle.eagle_variables import (download_button_id,
                                   pdf_viewer_class_name,
                                   stock_download_suffix)


def access_pdf_viewer(browser):
    try:
        pdf_viewer_present = EC.presence_of_element_located((By.CLASS_NAME, pdf_viewer_class_name))
        WebDriverWait(browser, long_timeout).until(pdf_viewer_present)
        pdf_viewer = browser.find_element_by_class_name(pdf_viewer_class_name)
        browser.switch_to.frame(pdf_viewer)
    except TimeoutException:
        print("Browser timed out while trying to access the pdf viewer.")


def execute_download(browser):
    try:
        download_button_present = EC.presence_of_element_located((By.ID, download_button_id))
        WebDriverWait(browser, long_timeout).until(download_button_present)
        download_button = browser.find_element_by_id(download_button_id)
        download_button.click()
        print("Executed download.")
    except TimeoutException:
        print("Browser timed out while trying to click the download button.")


def switch_to_browser_window(browser):
    browser.switch_to.default_content()


def determine_stock_download(document_number):
    return f'{document_number}-{stock_download_suffix}'


def download_document(browser, target_directory, county, document_number):
    access_pdf_viewer(browser)
    execute_download(browser)
    switch_to_browser_window(browser)
    document_directory = create_document_directory(target_directory)
    stock_download = determine_stock_download(document_number)
    if update_download(browser, county, stock_download, document_directory, document_number):
        return True
