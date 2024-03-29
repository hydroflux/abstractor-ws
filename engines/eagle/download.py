from selenium.common.exceptions import TimeoutException
from engines.eagle.disclaimer import check_for_disclaimer

from selenium_utilities.element_interaction import center_element
from selenium_utilities.inputs import click_button
from selenium_utilities.locators import (locate_element_by_class_name,
                                         locate_element_by_id)

from project_management.timers import naptime

from settings.iframe_handling import switch_to_default_content

# Use the following print statement to identify the best way to manage imports for Django vs the script folder
print("download", __name__)


def center_purchase_button(browser, abstract, document):
    purchase_button = locate_element_by_class_name(browser, abstract.county.classes["Purchase Button"],
                                                   "purchase button", clickable=True, document=document)
    center_element(browser, purchase_button)


def switch_into_frame(browser, abstract, document):
    try:
        pdf_viewer = locate_element_by_class_name(browser, abstract.county.classes["PDF Viewer"], "pdf viewer")
        if not pdf_viewer:
            # print('Unable to locate PDF viewer, trying again.')
            # print(f'PDF Viewer: {pdf_viewer}')
            # print(f'Reception Number: {document.reception_number}')
            # print(f'Download Value: {document.download_value}')
            return pdf_viewer
        center_purchase_button(browser, abstract, document)
        browser.switch_to.frame(pdf_viewer)
        return True
    except TimeoutException:
        print("Browser timed out while trying to access the pdf viewer, refreshing the page to try again.")
        return False


def access_pdf_viewer(browser, abstract, document):
    while not switch_into_frame(browser, abstract, document):
        # Is this function necessary with the 'check_for_disclaimer' function call at the top of the 'record' script?
        check_for_disclaimer(browser, abstract)
        print('Browser failed to access PDF viewer, refreshing and trying again...')
        browser.refresh()
        naptime()


def execute_download(browser, abstract, document):
    access_pdf_viewer(browser, abstract, document)
    while click_button(browser, locate_element_by_id,
                       abstract.county.buttons["Download Button"],
                       "download button", document) is False:
        print('Browser failed to access document image, refreshing and trying again...')
        browser.refresh()
        access_pdf_viewer(browser, abstract, document)
    switch_to_default_content(browser)
