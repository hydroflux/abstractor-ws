from selenium_utilities.inputs import click_button
from selenium_utilities.locators import locate_element_by_id

from settings.county_variables.rattlesnake import (add_to_cart_button_id,
                                                   download_page_id,
                                                   free_download_button_id)
from settings.download_management import update_download

from engines.rattlesnake.validation import (verify_document_image_page_loaded,
                                            verify_valid_download)


def handle_document_download_type(browser, abstract, document):
    if document.download_type == 'free':
        click_button(browser, locate_element_by_id, free_download_button_id,
                     "free download button", document)  # Click Free Download Button
        if verify_valid_download(browser):
            update_download(browser, abstract, document)
    elif document.download_type == 'paid':
        click_button(browser, locate_element_by_id, add_to_cart_button_id,
                     "add to cart button", document)  # Click Add To Cart Button


def execute_download(browser, abstract, document):
    click_button(browser, locate_element_by_id, download_page_id,
                 "download page button", document)  # Open Download Page
    if verify_document_image_page_loaded(browser, document):
    handle_document_download_type(browser, abstract, document)
