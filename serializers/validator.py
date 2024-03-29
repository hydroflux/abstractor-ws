from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.alert import Alert


def check_for_alert(browser, expected_alert):
    alert = Alert(browser)
    try:
        if alert.text == expected_alert:
            alert.accept()
            return True
        else:
            input(f'Encountered an unknown alert: "{alert.text}", please review and press enter to continue...')
    except NoAlertPresentException:
        return
