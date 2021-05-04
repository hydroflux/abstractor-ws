from pprint import pprint
from random import randint
from time import sleep

from settings.classes.counties import county_dictionary


def naptime():
    # sleep(randint(3, 6))
    sleep(randint(2, 3))


def short_nap():
    sleep(randint(1, 2))


def long_nap():
    sleep(randint(30, 45))


def get_county_data(county):
    return county_dictionary.get(county)


def scroll_into_view(browser, element):
    browser.execute_script("arguments[0].scrollIntoView();", element)


def javascript_script_execution(browser, script):
    browser.execute_script(script)


def get_element_text(element):
    return element.text.strip()


def title_strip(text):
    return text.title().strip()


# def scroll_to_top(browser):
#     try:
#         body_element_present = EC.presence_of_element_located((By.TAG_NAME, "body"))
#         WebDriverWait(browser, timeout).until(body_element_present)
#         body_element = browser.find_element_by_tag_name("body")
#         browser.execute_script("arguments[0].scrollIntoView();", body_element)
#     except TimeoutException:
#         print("Timed out while trying to scroll to the top of the page.")


def scroll_to_top(browser):
    body_element = browser.find_element_by_tag_name("body")
    scroll_into_view(browser, body_element)


def get_element_attributes(browser, element):
    attributes = browser.execute_script('var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;', element)
    pprint(attributes)