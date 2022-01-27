from project_management.export import export_document


def handle_single_document(browser, abstract, document, record, download_document):
    record(browser, abstract, document)
    if abstract.download and document.image_available and not abstract.review:
        download_document(browser, abstract, document)


def close_program(browser, abstract, logout=None):
    if logout is not None:
        logout(browser)
    if not abstract.download_only and not abstract.review:
        project = export_document(abstract)
        project.bundle_project(abstract)
    browser.close()
