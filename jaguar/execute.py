from settings.driver import create_webdriver
from settings.export import export_document
from settings.file_management import bundle_project


def search_documents_from_list(browser, target_directory, document_list):
    pass


def execute_program(county, target_directory, document_list, file_name):
    browser = create_webdriver(target_directory, False)
    # transform_document_list(document_list, county)
    # account_login(browser)
    abstraction = export_document(
        county,
        target_directory,
        file_name,
        search_documents_from_list(
            browser,
            target_directory,
            document_list,
        )
    )
    bundle_project(target_directory, abstraction)
    browser.close()
