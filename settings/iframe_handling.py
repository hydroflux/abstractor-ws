from selenium_utilities.locators import locate_elements_by_tag_name


def access_iframe_by_tag(browser):
    iframes = locate_elements_by_tag_name(browser, 'iframe', 'iframes')
    if len(iframes) == 0:
        print('Browser unable to locate any iframes on the page, please review.')
    elif len(iframes) > 1:
        print('Browser has located multiple iframes on the page, '
              'please attempt to access using a different method.')
    else:
        return iframes[0]


def switch_to_default_content(browser):
    browser.switch_to.default_content()
