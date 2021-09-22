from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from selenium_utilities.locators import locate_elements_by_tag_name

from settings.general_functions import timeout


def access_iframe_by_tag(browser):
    iframes = locate_elements_by_tag_name(browser, 'iframe', 'iframes')
    if len(iframes) == 0:
        print('Browser unable to locate any iframes on the page, please review.')
    elif len(iframes) > 1:
        print('Browser has located multiple iframes on the page, '
              'please attempt to access using a different method.')
    else:
        return iframes[0]


def locate_iframe_by_name(browser, iframe_name):
    try:
        iframe_present = EC.presence_of_element_located((By.NAME, iframe_name))
        WebDriverWait(browser, timeout).until(iframe_present)
        iframe = browser.find_element_by_name(iframe_name)
        return iframe
    except TimeoutException:
        print(f'Browser timed out trying to locate {iframe_name}, please review.')


def switch_to_default_content(browser):
    browser.switch_to.default_content()
