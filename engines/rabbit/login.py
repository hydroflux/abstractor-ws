from selenium_utilities.open import open_url
from engines.rabbit.disclaimer import handle_disclaimer


def login(browser, abstract):
    open_url(browser, abstract.county.urls["Home"], abstract.county.titles["Home"], "county site")
    handle_disclaimer(browser, abstract)
