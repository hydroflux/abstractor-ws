from engines.rattlesnake.open_document import open_document
from engines.rattlesnake.search import search


def next_result(browser, document):
    search(browser, document)
    open_document(browser, document)
