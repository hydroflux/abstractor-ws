from armadillo.armadillo_variables import logout_user_link


def logout(browser):
    browser.get(logout_user_link)
