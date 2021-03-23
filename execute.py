from dataframe import abstract_dataframe
from download import download_document
from open import open_document
from record import record_bad_search, record_document
from search import document_number_search


def search_documents_from_list(browser, document_list):
    for document_number in document_list:
        document_number_search(browser, document_number)
        if open_document(browser, document_number):
            record_document(browser, abstract_dataframe, document_number)
            download_document(browser)
            print(f'Document located at reception number {document_number} recorded, {len(document_list) - document_list.index(document_number)} documents remaining.')
        else:
            record_bad_search(abstract_dataframe, document_number)


def execute_script(browser, document_list):
    search_documents_from_list(browser, document_list)
    return abstract_dataframe
