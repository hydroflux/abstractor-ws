from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from settings.general_functions import timeout


def locate_iframes_by_tag(browser):
    try:
        iframes_present = EC.presence_of_element_located((By.TAG_NAME, 'iframe'))
        WebDriverWait(browser, timeout).until(iframes_present)
        iframes = browser.find_elements_by_tag_name('iframe')
        return iframes
    except TimeoutException:
        print('Browser timed out trying to locate iframes on the page, please review.')


def access_iframe_by_tag(browser):
    iframes = locate_iframes_by_tag(browser)
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
