from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from settings.download_management import previously_downloaded, update_download
from settings.file_management import (create_document_directory,
                                      extrapolate_document_value)
from settings.general_functions import (get_direct_link, long_timeout, naptime,
                                        newline_split, timeout)
from settings.iframe_handling import (access_iframe_by_tag,
                                      switch_to_default_content)
# from settings.error_handling import no_image_comment

from armadillo.armadillo_variables import (download_content_id,
                                           download_page_class_name, download_prefix)
from armadillo.validation import validate_download_link


def locate_download_page(browser, document):
    try:
        download_page_present = EC.element_to_be_clickable((By.CLASS_NAME, download_page_class_name))
        WebDriverWait(browser, timeout).until(download_page_present)
        download_page = browser.find_element_by_class_name(download_page_class_name)
        return download_page
    except TimeoutException:
        print(f'Browser timed out trying to locate download page for '
              f'{extrapolate_document_value(document)}, please review.')
        input()


def open_download_page(browser, document):
    download_page = locate_download_page(browser, document)
    download_page_link = get_direct_link(download_page)
    browser.get(download_page_link)


def switch_to_download_frame(browser, document):
    switch_to_default_content(browser)
    download_frame = access_iframe_by_tag(browser)
    browser.switch_to.frame(download_frame)


def locate_download_content(browser, document):
    try:
        download_content_present = EC.presence_of_element_located((By.ID, download_content_id))
        WebDriverWait(browser, timeout).until(download_content_present)
        download_content = browser.find_element_by_id(download_content_id)
        return download_content
    except TimeoutException:
        print(f'Browser timed out trying to locate download content for '
              f'{extrapolate_document_value(document)}, please review.')
        input()


def access_download_content(browser, document):
    switch_to_download_frame(browser, document)
    return locate_download_content(browser, document)


def access_listed_download_name(download_content):
    return newline_split(download_content.text)[0]


def verify_download(browser, document, download_content):
    listed_download_name = access_listed_download_name(download_content)
    if validate_download_link(document, listed_download_name):
        return True


def build_stock_download(document):
    return f'{download_prefix}{document.reception_number.replace("-", "_")}'


def free_download(browser):
    return True


def add_to_cart(browser, document):
    pass
    return True


def execute_download(browser, document_directory, document, download_type, download_content):
    if download_type == 'free':
        return free_download(browser, document_directory, document, download_content)
    elif download_type == 'paid':
        switch_to_default_content(browser)
        return add_to_cart(browser, document)


def download(browser, county, target_directory, document, download_type):
    document_directory = create_document_directory(target_directory)
    if previously_downloaded(county, document_directory, document.reception_number):
        return True
    else:
        open_download_page(browser, document)
        download_content = access_download_content(browser, document)
        if verify_download(browser, document):
            return execute_download(browser, document_directory, document, download_type, download_content)
