from engines.swordfish.open_document import open_document


def next_result(browser, abstract, document):
    browser.back()
    open_document(browser, abstract, document)