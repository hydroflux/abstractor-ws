from selenium_utilities.open import open_url


def open_document(browser, abstract, document):
    if abstract.program == "name_search":
        open_url(browser, document.description_link, abstract.county.titles["Search Result Page"],
                 f"reception number {document.reception_number} at {document.description_link}")