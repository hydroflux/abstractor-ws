from login import account_login
from search import document_number_search
from open import open_document
from record import record_document, record_bad_search
from download import download_document
from dataframe import abstract_dataframe

from time import sleep

def search_documents_from_list(browser, document_list):
    for document_number in document_list:
        document_number_search(browser, document_number)
        if open_document(browser, document_number):
            record_document(browser, abstract_dataframe, document_number)
            download_document(browser)
        else:
            record_bad_search(abstract_dataframe, document_number)

def execute_script(browser, document_list):
    account_login(browser)
    search_documents_from_list(browser, document_list)
    return abstract_dataframe