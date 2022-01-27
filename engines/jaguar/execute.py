from actions.executors import close_program, handle_single_document
from settings.invalid import record_invalid_search
from settings.driver import create_webdriver
from settings.general_functions import start_timer

from engines.jaguar.download import download_document
from engines.jaguar.login import account_login
from engines.jaguar.open_document import open_document
from engines.jaguar.record import record
from engines.jaguar.search import search
from engines.jaguar.transform import transform_document_list


def handle_multiple_documents(browser, abstract, document):
    print('Application not equipped to handle multiple documents at the moment; '
          'Script should not have reached this point, please review...')
    input()


# Identical to 'eagle', 'tiger', & 'leopard' handle_search_results
def handle_search_results(browser, abstract, document):
    if document.number_results == 1:
        handle_single_document(browser, abstract, document, record, download_document)
    elif document.number_results > 1:
        handle_multiple_documents(browser, abstract, document)


# Identical to 'eagle', 'tiger', & 'leopard' search_documents_from_list
def search_documents_from_list(browser, abstract):
    for document in abstract.document_list:
        document.start_time = start_timer()
        search(browser, document)
        if open_document(browser, document):
            handle_search_results(browser, abstract, document)
        else:
            record_invalid_search(abstract, document)


# Identical to 'leopard', 'tiger', & 'eagle' close_program
def execute_program(abstract):
    browser = create_webdriver(abstract)
    transform_document_list(abstract)
    account_login(browser)
    search_documents_from_list(browser, abstract)
    close_program(browser, abstract)
