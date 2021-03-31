from .search import search
from .open_document import open_document
from .record import record_document
from .download import download_document
from ..file_management import create_download_directory, remaining_downloads
from ..import_list import generate_document_list
from .login import account_login
from ..bad_search import record_bad_search
from ..abstract_object import abstract_dictionary as dictionary
from ..driver import chrome_webdriver
from ..export import export_document

from .variables import web_directory


def search_documents_from_list(browser, county, target_directory, document_list, download):
    for document_number in document_list:
        search(browser, document_number)
        if open_document(browser, document_number):
            record_document(browser, dictionary, document_number)
            if download:
                if not download_document(browser, county, target_directory, document_number):
                    dictionary["Comments"][-1] = f'No document image located at reception number {document_number}.'
        else:
            record_bad_search(dictionary, document_number)
            print(f'No document found at reception number {document_number}, {remaining_downloads(document_list, document_number)} documents remaining.')


def create_abstraction(browser, target_directory, file_name, sheet_name, download):
    document_list = generate_document_list(target_directory, file_name, sheet_name)
    search_documents_from_list(browser, document_list, download)
    return dictionary


def execute_web_program(client, legal, upload_file):
    sheet_name = 'Documents'
    download = True
    file_name = upload_file
    target_directory = web_directory
    browser = chrome_webdriver(target_directory, False)
    account_login(browser)
    dictionary = create_abstraction(browser, target_directory, file_name, sheet_name, download)
    export_document(target_directory, file_name, dictionary, client, legal)
    browser.close()
    return dictionary
