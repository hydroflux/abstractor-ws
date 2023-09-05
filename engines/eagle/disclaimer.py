from selenium.common.exceptions import NoSuchElementException


def locate_disclaimer(browser, abstract):
    try:
        disclaimer = browser.find_element("id", abstract.county.buttons["Disclaimer"])
        return disclaimer
    except NoSuchElementException:
        return False


def handle_disclaimer(browser, abstract):
    disclaimer = locate_disclaimer(browser, abstract)
    if not disclaimer:
        return True
    elif disclaimer.get_attribute(abstract.county.other["Inaccessible"]) is not None:
        return False
    elif disclaimer.get_attribute(abstract.county.other["Inaccessible"]) is None:
        disclaimer.click()
        return True


def check_for_disclaimer(browser, abstract):
    while not handle_disclaimer(browser, abstract):
        input('Disclaimer has not been handled properly, please press enter after resolving.')


# def check_for_disclaimer(browser, abstract):
#     while not handle_disclaimer(browser, abstract):
#         cookie = browser.get_cookie(abstract.county.other["Disclaimer Cookie"])
#         print("cookie", cookie)
#         if cookie == "false":
#             print('Encountered disclaimer, attempting to resolve...')
#             browser.delete_cookie(abstract.county.other["Disclaimer Cookie"])
#             browser.add_cookie({"name": abstract.county.other["Disclaimer Cookie"], "value": "true"})
#             browser.refresh()
        # input('Disclaimer has not been handled properly, please press enter after resolving.')
