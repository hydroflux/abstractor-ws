from project_management.export import export_document


def close_program(browser, abstract, logout_function=None):
    if logout_function is not None:
        logout_function(browser)
    if not abstract.download_only and not abstract.review:
        project = export_document(abstract)
        project.bundle_project(abstract)
    browser.close()
