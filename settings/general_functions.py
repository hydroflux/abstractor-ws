from random import randint
from time import sleep

if __name__ == '__main__':
    import settings.classes.counties as county_data
else:
    from .classes.counties import county_dictionary as county_data


def naptime():
    # sleep(randint(3, 6))
    sleep(randint(2, 3))


def get_county_data(county):
    return county_data.get(county)


def scroll_into_view(browser, element):
    browser.execute_script("arguments[0].scrollIntoView();", element)


def javascript_script_execution(browser, script):
    browser.execute_script(script)


def get_element_text(element):
    return element.text.strip()


def title_strip(text):
    return text.title().strip()
