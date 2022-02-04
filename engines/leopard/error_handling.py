# Used in leopard 'search' function
def check_for_browser_error(browser):
    if browser.title == "Error":
        print("Browser encountered an error during the search, refreshing the page to attempt to fix the problem.")
        # Review after hitting this error again, browser needs to still be logged in during error to see if this works
        browser.refresh()
