from selenium.common.exceptions import NoSuchElementException

from eagle.eagle_variables import disclaimer_id, inaccessible


def locate_disclaimer(browser):
    try:
        disclaimer = browser.find_element_by_id(disclaimer_id)
        return disclaimer
    except NoSuchElementException:
        return False


def handle_disclaimer(browser):
    disclaimer = locate_disclaimer(browser)
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
