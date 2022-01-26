import os

from selenium_utilities.inputs import click_button
from selenium_utilities.locators import locate_element_by_class_name

from settings.county_variables.jaguar import download_button_class
from settings.download_management import previously_downloaded, update_download
from settings.initialization import create_document_directory


# Nearly identical to 'leopard' prepare_for_download
def prepare_for_download(abstract, document):
    abstract.document_directory = create_document_directory(abstract.target_directory)
    abstract.document_directory_files = len(os.listdir(abstract.document_directory))
    document.download_value = f'{document.reception_number}.pdf'


# Very similar but not identical to 'leopard' execute_download
def execute_download(browser, abstract, document):
    click_button(browser, locate_element_by_class_name,  # Download Document
                 download_button_class, "download button", document)
    update_download(browser, abstract, document)


# Identical to 'leopard' & 'eagle' download_document
def download_document(browser, abstract, document):
    prepare_for_download(abstract, document)
    if not previously_downloaded(abstract, document):
        execute_download(browser, abstract, document)
