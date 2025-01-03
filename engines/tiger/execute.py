from serializers.executor import close_program, search_documents_from_list
from engines.tiger.transform import transform_document_list

from engines.tiger.download import execute_download
from engines.tiger.login import login
from engines.leopard.navigation import next_result
from engines.tiger.open_document import open_document
from engines.tiger.record import record
from engines.tiger.search import search

# Use the following print statement to identify the best way to manage imports for Django vs the script folder
print("execute", __name__)


# Identical to 'leopard', 'jaguar', 'rattlesnake', & 'eagle' execute_program
def execute_program(browser, abstract):
    transform_document_list(abstract)
    login(browser, abstract)
    search_documents_from_list(
        browser,
        abstract,
        search,
        open_document,
        record,
        execute_download,
        next_result
    )
    close_program(browser, abstract)
