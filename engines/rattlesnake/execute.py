from actions.executor import close_program, search_documents_from_list

from engines.rattlesnake.download import download_document
from engines.rattlesnake.download_early_documents import \
    download_early_documents
from engines.rattlesnake.login import account_login
from engines.rattlesnake.logout import logout
from engines.rattlesnake.open_document import open_document
from engines.rattlesnake.record import record
from engines.rattlesnake.search import search
from engines.rattlesnake.transform import transform_document_list

from settings.driver import create_webdriver


def next_result(browser, document):
    search(browser, document)
    open_document(browser, document)


def execute_program(abstract):
    browser = create_webdriver(abstract)
    transform_document_list(abstract, early_records=False)
    account_login(browser)
    search_documents_from_list(
        browser,
        abstract,
        search,
        open_document,
        record,
        download_document,
        next_result
    )
    close_program(browser, abstract, logout)


def execute_early_document_download(county, target_directory, document_list):
    browser = create_webdriver(target_directory, False)
    transform_document_list(document_list, county, True)
    account_login(browser)
    download_early_documents(browser, target_directory, document_list)
    browser.close()
