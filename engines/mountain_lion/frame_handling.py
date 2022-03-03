from selenium_utilities.locators import locate_element_by_name
from settings.iframe_handling import switch_to_default_content


def switch_to_main_frame(browser, abstract):
    switch_to_default_content(browser)
    main_frame = locate_element_by_name(browser, abstract.county.iframes['Main'], 'main iframe')
    browser.switch_to.frame(main_frame)
