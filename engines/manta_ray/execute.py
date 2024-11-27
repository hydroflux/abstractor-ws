#!/usr/bin/python3
from engines.manta_ray.collect import collect
from engines.manta_ray.download import execute_download
from engines.manta_ray.login import login
from engines.manta_ray.logout import logout
from engines.manta_ray.open_document import open_document
from engines.manta_ray.record import record
from engines.manta_ray.search import search
from engines.manta_ray.navigation import next_result

from serializers.executor import close_program, search_documents_from_list

# Same code functionality in "dolphin", "manta_ray", & "swordfish" (except for imports)


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
