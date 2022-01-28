from project_management.export import export_document
from settings.general_functions import start_timer
from settings.invalid import record_invalid_search


def handle_single_document(browser, abstract, document, record, download_document):
    record(browser, abstract, document)
    if abstract.download and document.image_available and not abstract.review:
        download_document(browser, abstract, document)


def handle_multiple_documents(browser, abstract, document, record, download_document, next_result):
    if next_result is None:
        print(f'{document.extrapolate_value()} returned "{document.number_results}" results; '
              f'Program not currently equipped to handle multiple documents at this point in time, '
              f'and script should not have reached this point; \n'
              f'Please review...')
        input()
    else:
        handle_single_document(browser, abstract, document, record, download_document)
        for result_number in range(1, document.number_results):
            document.result_number = result_number
            next_result(browser, document)
            handle_single_document(browser, abstract, document, record, download_document)


def handle_search_results(browser, abstract, document, record, download_document, next_result):
    if document.number_results == 1:
        handle_single_document(browser, abstract, document, record, download_document)
    elif document.number_results > 1:
        handle_multiple_documents(browser, abstract, document, record, download_document, next_result)


def search_documents_from_list(browser, abstract, search, open_document, record, download_document, next_result=None):
    for document in abstract.document_list:
        document.start_time = start_timer()
        search(browser, document)
        if open_document(browser, document):
            handle_search_results(browser, abstract, document, record, download_document, next_result)
        else:
            record_invalid_search(abstract, document)


def close_program(browser, abstract, logout=None):
    if logout is not None:
        logout(browser)
    if not abstract.download_only and not abstract.review:
        project = export_document(abstract)
        project.bundle_project(abstract)
    browser.close()
