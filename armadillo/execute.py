from settings.driver import create_webdriver

from armadillo.login import account_login


# Identical to crocodile execute_program
def execute_program(county, target_directory, document_list, file_name):
    browser = create_webdriver(target_directory, False)
    account_login(browser)
    # dictionary = search_documents_from_list(browser, county, target_directory, document_list)
    # logout(browser)
    # abstraction = export_document(county, target_directory, file_name, dictionary)
    # bundle_project(target_directory, abstraction)
    # browser.close()
