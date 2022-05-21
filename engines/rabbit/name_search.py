from classes.Document import Document
from engines.rabbit.search import search


def name_search(browser, abstract):
    document = Document("name", abstract.search_name)
    search(browser, abstract, document)
