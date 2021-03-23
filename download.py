from time import sleep

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from variables import (download_button_id, loading_status, long_timeout,
                       pdf_viewer_class_name, pdf_viewer_load_id)


def pdf_load_status(browser):
    try:
        pdf_viewer_loaded = EC.presence_of_element_located((By.ID, pdf_viewer_load_id))
        WebDriverWait(browser, long_timeout).until(pdf_viewer_loaded)
        return browser.find_element_by_id(pdf_viewer_load_id).text
    except TimeoutException:
        print("Browser timed out while waiting for the PDF Viewer to load.")


def wait_for_pdf_load(browser):
    while pdf_load_status(browser) == loading_status:
        sleep(0.5)
        pdf_load_status(browser)


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


def download_document(browser):
    wait_for_pdf_load(browser)
    access_pdf_viewer(browser)
    execute_download(browser)
    switch_to_browser_window(browser)
