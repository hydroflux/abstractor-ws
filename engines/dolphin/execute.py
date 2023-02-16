#!/usr/bin/python3
from engines.dolphin.collect import collect
from engines.dolphin.download import execute_download
from engines.dolphin.login import login
from engines.dolphin.logout import logout
from engines.dolphin.open_document import open_document
from engines.dolphin.record import record
from engines.dolphin.search import search

from serializers.executor import close_program, search_documents_from_list

# Same as "swordfish" except for imports


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
        execute_download
    )
    close_program(browser, abstract, logout)
