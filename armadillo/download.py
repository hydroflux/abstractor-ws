import os

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from selenium_utilities.inputs import center_element

from settings.download_management import previously_downloaded, update_download
from settings.file_management import (create_document_directory,
                                      extrapolate_document_value)
from settings.general_functions import (get_direct_link,
                                        newline_split, timeout)
from settings.iframe_handling import (access_iframe_by_tag,
                                      switch_to_default_content)

from armadillo.armadillo_variables import (add_to_cart_name,
                                           download_content_id,
                                           download_page_class_name,
                                           download_prefix,
                                           free_download_button_tag)


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


# def verify_download(browser, document):
#     download_content = access_download_content(browser, document)
#     listed_download_name = access_listed_download_name(download_content)
#     return validate_download_link(document, listed_download_name)


def locate_free_download_button(download_content, document):
    try:
        free_download_button_present = EC.element_to_be_clickable((By.TAG_NAME, free_download_button_tag))
        WebDriverWait(download_content, timeout).until(free_download_button_present)
        free_download_button = download_content.find_element_by_tag_name(free_download_button_tag)
        return free_download_button
    except TimeoutException:
        print(f'Browser timed out trying to locate free download button for '
              f'{extrapolate_document_value(document)}, please review.')
        input()


def access_free_download_button(download_content, document):
    free_download_button = locate_free_download_button(download_content, document)
    return get_direct_link(free_download_button)


def build_stock_download(document):
    document.download_value = f'{download_prefix}{document.download_value}.pdf'


def free_download(browser, document):
    download_content = access_download_content(browser, document)
    free_download_link = access_free_download_button(download_content, document)
    switch_to_default_content(browser)
    browser.get(free_download_link)


def locate_add_to_cart_form(browser, document):
    try:
        add_to_cart_form_present = EC.presence_of_element_located((By.NAME, add_to_cart_name))
        WebDriverWait(browser, timeout).until(add_to_cart_form_present)
        add_to_cart_form = browser.find_element_by_name(add_to_cart_name)
        return add_to_cart_form
    except TimeoutException:
        print(f'Browser timed out trying to locate "Add to Cart" form for '
              f'{extrapolate_document_value(document)}, please review.')
        input()


def add_to_cart(browser, document):
    add_to_cart_form = locate_add_to_cart_form(browser, document)
    center_element(browser, add_to_cart_form)
    add_to_cart_form.submit()
    return True


def execute_download(browser, document_directory, document):
    if document.download_type == 'free':
        number_files = len(os.listdir(document_directory))
        free_download(browser, document)
        build_stock_download(document)
        return update_download(
            browser,
            document_directory,
            document,
            number_files
            )
    elif document.download_type == 'paid':
        return add_to_cart(browser, document)


def check_last_document(dataframe, document, result_number, count=0):
    if result_number > 0:
        for element in dataframe["Document Link"]:
            if element == dataframe["Document Link"][-1]:
                count += 1
            elif element == f'{dataframe["Document Link"][-1]}-{str(count)}':
                count += 1
        if count > 1:
            dataframe["Document Link"][-1] = f'{dataframe["Document Link"][-1]}-{str(count - 1)}'
            document.new_name = f'{document.new_name[:-4]}-{str(count - 1)}.pdf'
        else:
            return True
    else:
        return True


def download_document(browser, target_directory, dataframe, document, result_number):
    document_directory = create_document_directory(target_directory)
    if previously_downloaded(document_directory, document):
        if check_last_document(dataframe, document, result_number):
            return True
    open_download_page(browser, document)
    # if verify_download(browser, document):
    switch_to_default_content(browser)
    return execute_download(browser, document_directory, document)
