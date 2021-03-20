from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from variables import timeout, pdf_viewer_class_name, download_button_id

def access_pdf_viewer(browser):
    try:
        pdf_viewer_present = EC.presence_of_element_located((By.CLASS_NAME, pdf_viewer_class_name))
        WebDriverWait(browser, timeout).until(pdf_viewer_present)
        pdf_viewer = browser.find_element_by_class_name(pdf_viewer_class_name)
        browser.switch_to.frame(pdf_viewer)
    except TimeoutException:
        print("Browser timed out while trying to access the pdf viewer.")

def execute_download(browser):
    try:
        download_button_present = EC.presence_of_element_located((By.ID, download_button_id))
        WebDriverWait(browser, timeout).until(download_button_present)
        download_button = browser.find_element_by_id(download_button_id)
        download_button.click()
    except TimeoutException:
        print("Browser timed out while trying to click the download button.")

def switch_out_of_pdf_viewer(browser):
    browser.switch_to.default_content()

def download_document(browser):
    access_pdf_viewer(browser)
    execute_download(browser)
    switch_out_of_pdf_viewer(browser)