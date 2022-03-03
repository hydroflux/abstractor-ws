from engines.mountain_lion.iframe_handling import switch_to_main_frame
from selenium_utilities.locators import locate_element_by_id


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
