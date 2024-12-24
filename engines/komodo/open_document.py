from selenium_utilities.open import open_url


def next_result(browser, abstract, document):
    print(f"Processing result number {document.result_number + 1} of {document.number_results}...")
    return open_document(browser, abstract, document)


def open_document(browser, abstract, document):
    if abstract.program == "name_search":
        open_url(browser, document.description_link, abstract.county.titles["Search Result Page"],
                 f"reception number {document.reception_number} at {document.description_link}")
        return True
    elif abstract.program in ["execute", "review"]:
        open_url(browser, document.result_links[document.result_number], abstract.county.titles["Search Result Page"],
                 f"reception number {document.reception_number} at {document.description_link}")
        return True
    else:
        input(f"""No open document function for a "{abstract.program}" program type, """
              f"""please review and enter to continue...""")
