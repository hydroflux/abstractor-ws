from selenium.common.exceptions import StaleElementReferenceException


def center_element(browser, element):
    try:
        desired_y = (element.size['height'] / 2) + element.location['y']
        window_h = browser.execute_script('return window.innerHeight')
        window_y = browser.execute_script('return window.pageYOffset')
        current_y = (window_h / 2) + window_y
        scroll_y_by = desired_y - current_y
        browser.execute_script("window.scrollBy(0, arguments[0]);", scroll_y_by)
    except StaleElementReferenceException:
        print('Browser encountered a StaleElementReferenceException while trying to center '
              'element, please review and press enter to continue...')
        input()


def is_active_class(element):
    element_class = element.get_attribute("class")
    if element_class.endswith("active"):
        return True


def get_parent_element(element):
    return element.find_element_by_xpath("..")


# move out of 'general_functions' & update dependencies
def get_element_text(element):
    return element.text
