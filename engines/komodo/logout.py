from selenium_utilities.open import open_url

def logout(browser, abstract):
    open_url(
        browser,
        abstract.county.urls["Logout Page"],
        abstract.county.titles["Logout Page"],
        "logout page"
    )