from engines.mountain_lion.iframe_handling import switch_to_main_frame
from engines.mountain_lion.validation import page_is_loaded
from selenium_utilities.inputs import click_button
from selenium_utilities.locators import locate_element_by_id


def open_search_page(browser, abstract, document):
    browser.refresh()
    switch_to_main_frame(browser, abstract)
    click_button(browser, locate_element_by_id,
                 abstract.county.buttons['Open Search'], "open search", document)


def process_document_search(browser, document):
    pass


def search(browser, abstract, document):
    open_search_page(browser, abstract, document)
    if page_is_loaded(browser, abstract, abstract.county.messages['Search Header']):
        process_document_search(browser, document)
