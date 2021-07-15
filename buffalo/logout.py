from settings.general_functions import javascript_script_execution

from buffalo.buffalo_variables import logout_script
from buffalo.frame_handling import switch_to_default_content


def log_out_user(browser):
    switch_to_default_content(browser)    
    javascript_script_execution(browser, logout_script)


def verify_logout(browser):
    pass


def logout(browser):
    log_out_user(browser)
    verify_logout(browser)
    browser.quit()
    exit()
