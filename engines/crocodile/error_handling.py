from selenium_utilities.open import assert_window_title
from settings.dataframe_management import extrapolate_document_value

from settings.county_variables.crocodile import website_title

from engines.crocodile.login import account_login


def check_login_status(browser, document):
    if assert_window_title(browser, website_title):
        print(f'Browser appears to have encountered a logout error while searching '
              f'{extrapolate_document_value(document)}, attempting to log back in.')
        account_login(browser)
        return True
    else:
        print('Browser has encountered an unknown error, please review.')
