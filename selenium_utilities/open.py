def assert_window_title(browser, page_title):
    try:
        assert page_title in browser.title.strip()
        return True
    except AssertionError:
        return False


def print_failed_window_assertion_statement(page_type, document):
    if document is None:
        print(f'Browser failed to successfully open {page_type}, please review.')
    else:
        print(f'Browser failed to successfully open {page_type}, please review.')


def open_url(browser, url, page_title, page_type, document=None):
    browser.get(url)
    if not assert_window_title(browser, page_title):
        print_failed_window_assertion_statement(page_type, document)
