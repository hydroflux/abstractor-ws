#!/usr/bin/python3
from engines.octopus.collect import collect
from engines.octopus.download import execute_download
from engines.octopus.login import login
from engines.octopus.logout import logout
from engines.octopus.open_document import open_document
from engines.octopus.record import record
from engines.octopus.search import search

from serializers.executor import close_program, search_documents_from_list


def check_for_document_list(browser, abstract):
    if abstract.program in ['name_search', 'legal']:
        search(browser, abstract)
        collect(browser, abstract)


def execute_legal_search(browser, abstract):
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
