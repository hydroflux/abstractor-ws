from selenium_utilities.open import open_url


def login(browser, abstract):
    open_url(browser, abstract.county.urls["Home"], abstract.county.titles["Home"], "county site")
