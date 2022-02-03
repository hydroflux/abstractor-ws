from serializers.executor import close_program, search_documents_from_list

from settings.driver import create_webdriver

from engines.jaguar.download import execute_download
from engines.jaguar.login import account_login
from engines.jaguar.open_document import open_document
from engines.jaguar.record import record
from engines.jaguar.search import search


# Identical to 'leopard', 'tiger', 'rattlesnake', & 'eagle' execute_program
def execute_program(abstract):
    browser = create_webdriver(abstract)
    # transform_document_list(abstract)
    account_login(browser)
    search_documents_from_list(
        browser,
        abstract,
        search,
        open_document,
        record,
        execute_download,
        next_result=None
    )
    close_program(browser, abstract)
