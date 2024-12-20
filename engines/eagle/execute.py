#!/usr/bin/python3
from engines.eagle.name_search import name_search
from serializers.executor import close_program, search_documents_from_list

from engines.eagle.download import execute_download
from engines.eagle.login import login
from engines.eagle.navigation import next_result
from engines.eagle.open_document import open_document
from engines.eagle.record import record
from engines.eagle.search import search


# Identical to 'leopard', 'jaguar', 'rattlesnake', & 'tiger' execute_program
def execute_program(browser, abstract):
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


def execute_name_search(browser, abstract):
    login(browser, abstract)
    name_search(browser, abstract)
    close_program(browser, abstract)
