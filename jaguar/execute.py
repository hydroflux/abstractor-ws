from settings.bad_search import record_bad_search
from settings.driver import create_webdriver
from settings.export import export_document
from settings.general_functions import start_timer

from jaguar.download import download_document
from jaguar.login import account_login
from jaguar.open_document import open_document
from jaguar.record import record
from jaguar.search import search
from jaguar.transform import transform_document_list


def handle_single_document(browser, abstract, document):
    record(browser, abstract, document)
    if abstract.download and not abstract.review:
        download_document(browser, abstract, document)


def handle_multiple_documents(browser, abstract, document):
    print('Application not equipped to handle multiple documents at the moment; '
          'Script should not have reached this point, please review...')
    input()


# Identical to 'eagle' execute_program
def handle_search_results(browser, abstract, document):
    if document.number_results == 1:
        handle_single_document(browser, abstract, document)
    elif document.number_results > 1:
        handle_multiple_documents(browser, abstract, document)


# Identical to 'eagle' execute_program
def search_documents_from_list(browser, abstract):
    for document in abstract.document_list:
        document.start_time = start_timer()
        search(browser, document)
        if open_document(browser, document):
            handle_search_results(browser, abstract, document)
        else:
            record_bad_search(abstract, document)


# Identical to 'eagle' execute_program
def execute_program(abstract):
    browser = create_webdriver(abstract)
    transform_document_list(abstract)
    account_login(browser)
    search_documents_from_list(browser, abstract)
    project = export_document(abstract)
    project.bundle_project()
    browser.close()
