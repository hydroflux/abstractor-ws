import sys
from settings.initialization import initialize_abstraction

from settings.driver import create_webdriver

# ADJUST ENGINE PROFILE TO CHANGE DEVELOPMENT SETTING
from engines.buffalo.login import login
from engines.buffalo.search import search
from engines.buffalo.logout import logout

sys.path.append(".")


def execute_program_functions(browser, abstract, document=None):
    login(browser, abstract)
    search(browser, abstract, document)
    if None:
        logout(browser, abstract)


def execute_developer():
    # need an initialize development function to avoid imports
    abstract = initialize_abstraction()
    browser = create_webdriver(abstract)
    document = abstract.document_list[0]
    execute_program_functions(browser, abstract, document)
    return browser, abstract, document


browser, abstract, document = execute_developer()
