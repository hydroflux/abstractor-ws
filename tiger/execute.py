from .search import search
from .open_document import open_document
from .record import record_document
from .download import download_document
from ..abstract_object import abstract_dictionary as dictionary
from ..file_management import create_download_directory, remaining_downloads
from ..bad_search import record_bad_search


def search_documents_from_list(browser, document_list, download):
    for document_number in document_list:
        search(browser, document_number)
        if open_document(browser, document_number):
            record_document(browser, dictionary, document_number)
            if download:
                if not download_document(browser, county, document_directory, document_number):
                    dictionary["Comments"][-1] = f'No document image located at reception number {document_number}.'
        else:
            record_bad_search(dictionary, document_number)
            print(f'No document found at reception number {document_number}, {remaining_downloads(document_list, document_number)} documents remaining.')