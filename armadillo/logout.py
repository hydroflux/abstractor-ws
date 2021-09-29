from settings.county_variables.armadillo import logout_user_link


def logout(browser):
    browser.get(logout_user_link)
