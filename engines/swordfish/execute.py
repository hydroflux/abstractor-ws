#!/usr/bin/python3
from engines.swordfish.collect import collect
from engines.swordfish.download import execute_download
from engines.swordfish.login import login
from engines.swordfish.logout import logout
from engines.swordfish.open_document import open_document
from engines.swordfish.record import record
from engines.swordfish.search import search
from engines.swordfish.navigation import next_result

from serializers.executor import close_program, search_documents_from_list

# Same as "dolphin" except for imports


def check_for_document_list(browser, abstract):
    if abstract.program in ['name_search', 'legal']:
        search(browser, abstract)
        collect(browser, abstract)


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
