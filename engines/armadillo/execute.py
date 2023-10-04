#!/usr/bin/python3
from engines.armadillo.name_search import name_search
from project_management.export import export_document
from serializers.executor import close_program, search_documents_from_list

from engines.armadillo.download import execute_download
from engines.armadillo.login import login
from engines.armadillo.navigation import next_result
from engines.armadillo.open_document import open_document
from engines.armadillo.record import record
from engines.armadillo.search import search


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
    project = export_document(abstract)  # handled in close_program, need to review
    project.bundle_project(abstract)  # handled in close_program, need to review
    close_program(browser, abstract)
