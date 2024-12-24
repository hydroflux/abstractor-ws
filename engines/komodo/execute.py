#!/usr/bin/python3
from engines.komodo.download import execute_download
from engines.komodo.login import login
from engines.komodo.logout import logout
from engines.komodo.open_document import next_result, open_document
from engines.komodo.record import record
from engines.komodo.search import search
# from engines.komodo.navigation import next_result

from serializers.executor import close_program, search_documents_from_list

# Same code functionality in "dolphin", "manta_ray", & "swordfish" (except for imports)


def check_for_document_list(browser, abstract):
    if abstract.program in ['name_search', 'legal']:
        search(browser, abstract)


def execute_program(browser, abstract):
    login(browser, abstract)
    check_for_document_list(browser, abstract)
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
