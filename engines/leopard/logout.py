from selenium_utilities.locators import locate_element_by_id


def access_logout_link(browser, abstract):
    logout_button = locate_element_by_id(browser, abstract.county.buttons["Logout"],
                                         "logout button", True)
    return logout_button.get_attribute("href")


def logout(browser, abstract):
    logout_link = access_logout_link(browser, abstract)
    browser.get(logout_link)
