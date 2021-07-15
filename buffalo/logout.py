def log_out_user(browser):
    pass


def verify_logout(browser):
    pass


def logout(browser):
    log_out_user(browser)
    verify_logout(browser)
    browser.quit()
    exit()
