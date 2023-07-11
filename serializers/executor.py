from serializers.downloader import download_document

from project_management.export import export_document
from project_management.timers import start_timer

# from settings.driver import create_webdriver
from settings.invalid import record_invalid_search


def handle_single_document(browser, abstract, document, record, execute_download):
    record(browser, abstract, document)
    abstract.report_document_found(document)
    abstract.check_last_document(document)  # should download be skipped if last document is a duplicate
    if abstract.download and document.image_available and not abstract.review:
        download_document(browser, abstract, document, execute_download)
    if abstract.download_only is False:
        abstract.check_length()  # Is this the best placement for this?


def handle_multiple_documents(browser, abstract, document, record, execute_download, next_result):
    if next_result is None:
        print(f'{document.extrapolate_value()} returned "{document.number_results}" results; '
              f'Program not currently equipped to handle multiple documents at this point in time, '
              f'and script should not have reached this point; \n'
              f'Please review...')
        input()
    else:
        handle_single_document(browser, abstract, document, record, execute_download)
        for result_number in range(1, document.number_results):
            document.result_number = result_number
            next_result(browser, abstract, document)
            handle_single_document(browser, abstract, document, record, execute_download)


def handle_search_results(browser, abstract, document, record, execute_download, next_result):
    if document.number_results == 1:
        handle_single_document(browser, abstract, document, record, execute_download)
    elif document.number_results > 1:
        handle_multiple_documents(browser, abstract, document, record, execute_download, next_result)
    else:
        print(f'{document.extrapolate_value()} returned "{str(document.number_results)}" results, '
              f'which is not applicable for the "handle_search_results" function structure; Please review...')
        input()


def search_documents_from_list(browser, abstract, search, open_document, record, execute_download, next_result=None):
    for document in abstract.document_list:
        document.start_time = start_timer()
        search(browser, abstract, document)
        if open_document(browser, abstract, document):
            handle_search_results(browser, abstract, document, record, execute_download, next_result)
        else:
            if abstract.program != "register_page_count":
                record_invalid_search(abstract, document)


def close_program(browser, abstract, logout=None):
    if logout is not None:
        logout(browser, abstract)
    if not abstract.download_only and not abstract.review:
        project = export_document(abstract)
        project.bundle_project(abstract)
    browser.close()


# def execute_program(abstract, transform, login, search, open_document, record,
#                     execute_download, next_result=None, logout=None):
#     browser = create_webdriver(abstract)
#     transform(abstract)
#     login(browser, abstract)
#     search_documents_from_list(
#         browser,
#         abstract,
#         search,
#         open_document,
#         record,
#         execute_download,
#         next_result
#     )
#     close_program(browser, abstract, logout)
