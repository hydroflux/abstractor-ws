import os

from selenium_utilities.inputs import click_button
from selenium_utilities.locators import locate_element_by_class_name

from settings.download_management import previously_downloaded, update_download
from settings.county_variables.jaguar import download_button_class


def execute_download(browser, document_directory, document):
    document.download_value = f'{document.reception_number}.pdf'
    number_files = len(os.listdir(document_directory))
    click_button(browser, locate_element_by_class_name, download_button_class, "download button", document)
    return update_download(
        browser,
        document_directory,
        document,
        number_files
    )


def download_document(browser, document_directory, document):
    if previously_downloaded(document_directory, document):
        return True
    else:
        return execute_download(browser, document_directory, document)
