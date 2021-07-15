from settings.general_functions import (assert_window_title,
                                        javascript_script_execution)

from buffalo.buffalo_variables import logout_script, website_title
from buffalo.frame_handling import switch_to_default_content


def log_out_user(browser):
    switch_to_default_content(browser)    
    javascript_script_execution(browser, logout_script)


def verify_logout(browser):
    if not assert_window_title(browser, website_title):
        print('Browser failed to successfully log out user, please review.')
        input()
    else:
        return True


def logout(browser):
    log_out_user(browser)
    if verify_logout(browser):
        browser.quit()
        exit()
