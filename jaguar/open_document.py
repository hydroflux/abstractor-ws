from jaguar.validation import verify_search_results_page_loaded, verify_results_loaded

def count_results(browser, document):
    pass


def handle_search_results(browser, document):
    pass


def open_document(browser, document):
    # verify_search_results_page_loaded(browser, document)
    if verify_results_loaded(browser, document):
        count_results(browser, document)
        return handle_search_results(browser, document)
    else:
        return False
