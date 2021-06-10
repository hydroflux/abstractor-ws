from settings.general_functions import assert_window_title
from settings.file_management import extrapolate_document_value

from crocodile.crocodile_variables import website_title
from crocodile.login import account_login


def check_login_status(browser, document):
    if assert_window_title(browser, website_title):
        print(f'Browser appears to have encountered a logout error while searching '
              f'{extrapolate_document_value(document)}, attempting to log back in.')
        account_login(browser)
    else:
        print(f'Browser has encountered an unknown error, please review.')
