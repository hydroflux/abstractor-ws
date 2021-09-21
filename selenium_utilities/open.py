def assert_window_title(browser, window_title):
    try:
        assert window_title in browser.title.strip()
        return True
    except AssertionError:
        return False
