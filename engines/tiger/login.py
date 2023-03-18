from selenium.webdriver.common.keys import Keys
from engines.tiger.disclaimer import handle_disclaimer
# from selenium_utilities.inputs import click_button, enter_input_value
from selenium_utilities.locators import (locate_element_by_id, locate_element_by_class_name)
#  locate_element_by_name)
# from selenium_utilities.open import open_url

# from engines.tiger.search import open_search


def open_site(browser, abstract):
    browser.get(abstract.county.urls["Login"])
    assert abstract.county.titles["Login"] in browser.title


def enter_credentials(browser, abstract):
    login_prompt = locate_element_by_id(browser, abstract.county.credentials[0], "login prompt")
    login_prompt.send_keys(abstract.county.credentials[1] + Keys.TAB + abstract.county.credentials[3] + Keys.RETURN)


# def enter_credentials(browser, abstract):
#     enter_input_value(browser,
#                       locate_element_by_id,
#                       abstract.county.credentials[0],
#                       "username input",
#                       abstract.county.credentials[1])
#     enter_input_value(browser,
#                       locate_element_by_id,
#                       abstract.county.credentials[2],
#                       "password input",
#                       abstract.county.credentials[3])
#     click_button(browser,
#                  locate_element_by_name,
#                  abstract.county.buttons["Login"],
#                  "login button")


def verify_login(browser, abstract):
    if browser.title == abstract.county.titles["Login"]:
        validation_errors = locate_element_by_class_name(browser, abstract.county.classes["Validation Error"],
                                                         "validation errors")
        print(validation_errors.text)
        browser.quit()
        exit()


def login(browser, abstract):
    open_site(browser, abstract)
    print("1")
    enter_credentials(browser, abstract)
    print("2")
    verify_login(browser, abstract)
    print("3")
    handle_disclaimer(browser, abstract)


# def login(browser, abstract):
#     open_url(browser,
#              abstract.county.urls["Login"],
#              abstract.county.titles["Login"],
#              "county site")
#     enter_credentials(browser, abstract)
#     open_search(browser, abstract)
#     click_button(browser,  # Handle Disclaimer
#                  locate_element_by_id,
#                  abstract.county.buttons["Disclaimer"],
#                  "login disclaimer")
