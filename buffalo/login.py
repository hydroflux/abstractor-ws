from settings.general_functions import assert_window_title, timeout

from buffalo.buffalo_variables import (credentials, website, website_title)


def open_site(browser):
    browser.get(website)
    if not assert_window_title(browser, website_title):
        print('Browser failed to successfully open site, please review.')
        browser.close()
        quit()
