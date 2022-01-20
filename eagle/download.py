import os

from selenium.common.exceptions import TimeoutException

from selenium_utilities.inputs import click_button
from selenium_utilities.locators import (locate_element_by_class_name,
                                         locate_element_by_id)

from settings.county_variables.eagle import (pdf_viewer_class_name,
                                             stock_download_suffix)
from settings.download_management import previously_downloaded, update_download
from settings.error_handling import no_image_comment
from settings.general_functions import naptime
from settings.iframe_handling import switch_to_default_content

# Use the following print statement to identify the best way to manage imports for Django vs the script folder
print("download", __name__)


def download_available(dataframe, document):
    if dataframe["Comments"][-1].endswith(no_image_comment(document)):
        print(no_image_comment(document))
        return False
    else:
        return True


def switch_into_frame(browser, document):
    try:
        pdf_viewer = locate_element_by_class_name(browser, pdf_viewer_class_name, "pdf viewer")
        if not pdf_viewer:
            print('Unable to locate PDF viewer, trying again.')
            print(f'PDF Viewer: {pdf_viewer}')
            print(f'Reception Number: {document.reception_number}')
            print(f'Download Value: {document.download_value}')
            return pdf_viewer
        browser.switch_to.frame(pdf_viewer)
        return True
    except TimeoutException:
        print("Browser timed out while trying to access the pdf viewer, refreshing the page to try again.")
        return False


def access_pdf_viewer(browser, document):
    while not switch_into_frame(browser, document):
        browser.refresh()
        naptime()


# def execute_download(browser):
#     try:
#         download_button_present = EC.presence_of_element_located((By.ID, download_button_id))
#         WebDriverWait(browser, long_timeout).until(download_button_present)
#         download_button = browser.find_element_by_id(download_button_id)
#         download_button.click()
#         print("Executed download.")
#     except TimeoutException:
#         print("Browser timed out while trying to click the download button.")


def build_stock_download(document):
    document.download_value = f'{document.reception_number}-{stock_download_suffix}'


def check_last_download(dataframe, document, count=0):
    if document.result_number > 0:
        for element in dataframe["Reception Number"]:
            if element == dataframe["Reception Number"][-1]:
                count += 1
            elif element == f'{dataframe["Reception Number"][-1]}-{str(count)}':
                count += 1
        if count > 1:
            dataframe["Reception Number"][-1] = f'{dataframe["Reception Number"][-1]}-{str(count - 1)}'
            document.new_name = f'{document.county.prefix}-{document.reception_number}-{str(count - 1)}.pdf'
        else:
            return True
    else:
        return True


def execute_download(browser, dataframe, document_directory, document):
    number_files = len(os.listdir(document_directory))
    build_stock_download(document)
    access_pdf_viewer(browser, document)
    click_button(browser, locate_element_by_id, document.button_attributes["Download Button"], "download button")
    switch_to_default_content(browser)
    return update_download(
        browser,
        document_directory,
        document,
        number_files
    )


def download_document(browser, abstract, document):
    if download_available(dataframe, document):
        if previously_downloaded(document_directory, document):
            if check_last_download(dataframe, document):
                return True
        return execute_download(browser, dataframe, document_directory, document)
