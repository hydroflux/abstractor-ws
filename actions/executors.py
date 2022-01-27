from project_management.export import export_document


def handle_single_document(browser, abstract, document, record, download_document):
    record(browser, abstract, document)
    if abstract.download and document.image_available and not abstract.review:
        download_document(browser, abstract, document)


def handle_multiple_documents(browser, abstract, document, record, download_document, next_result=None):
    if next_result is None:
        print(f'{document.extrapolate_value()} returned "{document.number_results}" results; '
              f'Program not currently equipped to handle multiple documents at this point in time, '
              f'please review...')
        input()
    else:
        handle_single_document(browser, abstract, document, record, download_document)
        for result_number in range(1, document.number_results):
            document.result_number = result_number
            next_result(browser, document)
            handle_single_document(browser, abstract, document, record, download_document)


def close_program(browser, abstract, logout=None):
    if logout is not None:
        logout(browser)
    if not abstract.download_only and not abstract.review:
        project = export_document(abstract)
        project.bundle_project(abstract)
    browser.close()
