from engines.mountain_lion.iframe_handling import switch_to_header_frame, switch_to_main_frame
from selenium_utilities.locators import locate_element_by_id, locate_element_by_tag_name


def validate_login(browser, abstract):
    switch_to_main_frame(browser, abstract)
    welcome_message = locate_element_by_id(browser, abstract.county.ids['Post Login'], 'post login')
    if welcome_message.text.strip() == abstract.county.messages['Post Login']:
        print('\nLogin successful, continuing program execution.')
    else:
        # print('\nBrowser failed to successfully login, exiting program.')
        # browser.quit()
        # exit()
        print('\nBrowser failed to successfully login, please review...')
        input()


def header_validation(browser, abstract, validation_text):
    switch_to_header_frame(browser, abstract)
    element_text = locate_element_by_tag_name(browser, abstract.county.tags['Header Text'], 'header text')
    return element_text.startswith(validation_text)


def page_is_loaded(browser, abstract, validation_text):
    if not header_validation(browser, abstract, validation_text):
        print(f'Browser indicates that it has not properly loaded '
              f'"{validation_text}", please review webdriver before continuing...')
        input()
    else:
        return True
