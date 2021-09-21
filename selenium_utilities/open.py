def assert_window_title(browser, page_title):
    try:
        assert page_title in browser.title.strip()
        return True
    except AssertionError:
        return False


def print_failed_window_assertion_statement(page_type, document):
    if document is None:
        print(f'Browser failed to successfully open "{page_type}", please review.')
    else:
        print(f'Browser failed to successfully open "{page_type}" for '
              f'{document.extrapolate_value()}, please review.')


def handle_failed_window_assertion(browser, page_type, document):
    print_failed_window_assertion_statement(page_type, document)
    if page_type == 'county site':
        browser.close()
        quit()


def open_url(browser, url, page_title, page_type, document=None):
    browser.get(url)
    if not assert_window_title(browser, page_title):
        handle_failed_window_assertion(browser, page_type, document)
