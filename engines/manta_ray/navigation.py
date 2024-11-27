from engines.manta_ray.open_document import open_document

# Exact same code functionality as "swordfish"

def next_result(browser, abstract, document):
    browser.back()
    open_document(browser, abstract, document)
