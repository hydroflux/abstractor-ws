from serializers.executor import close_program, search_documents_from_list

from engines.rattlesnake.download import execute_download
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


# Identical to 'tiger', 'jaguar', 'leopard', & 'eagle' execute_program
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
        execute_download,
        next_result
    )
    close_program(browser, abstract, logout)


def execute_early_document_download(abstract):
    browser = create_webdriver(abstract)
    transform_document_list(abstract, True)
    account_login(browser)
    download_early_documents(browser, abstract)
    browser.close()
