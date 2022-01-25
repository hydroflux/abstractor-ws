import os

from selenium_utilities.inputs import click_button
from selenium_utilities.locators import locate_element_by_class_name
from settings.initialization import create_document_directory
from settings.invalid import no_download

from settings.download_management import previously_downloaded, update_download
from settings.county_variables.jaguar import download_button_class
from settings.file_management import document_downloaded


def execute_download(browser, abstract, document):
    document.download_value = f'{document.reception_number}.pdf'
    number_files = len(os.listdir(abstract.document_directory))
    click_button(browser, locate_element_by_class_name, download_button_class, "download button", document)
    if update_download(
        browser,
        abstract.document_directory,
        document,
        number_files
    ):
        document_downloaded(abstract.document_list, document)
    else:
        no_download(abstract, document)


def download_document(browser, abstract, document):
    abstract.document_directory = create_document_directory(abstract.target_directory)
    if previously_downloaded(abstract, document):
        document_downloaded(abstract.document_list, document)
        return True
    else:
        execute_download(browser, abstract, document)
