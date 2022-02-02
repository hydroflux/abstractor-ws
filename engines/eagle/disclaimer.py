from selenium.common.exceptions import NoSuchElementException

from settings.county_variables.eagle import inaccessible


def locate_disclaimer(browser, abstract):
    try:
        disclaimer = browser.find_element_by_id(abstract.county.buttons["Disclaimer"])
        return disclaimer
    except NoSuchElementException:
        return False


def handle_disclaimer(browser, abstract):
    disclaimer = locate_disclaimer(browser, abstract)
    if not disclaimer:
        return True
    elif disclaimer.get_attribute(inaccessible) is not None:
        return False
    elif disclaimer.get_attribute(inaccessible) is None:
        disclaimer.click()
        return True


def check_for_disclaimer(browser):
    while not handle_disclaimer(browser):
        input('Disclaimer has not been handled properly, please press enter after resolving.')
