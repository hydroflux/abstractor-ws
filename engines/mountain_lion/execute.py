from serializers.executor import close_program, search_documents_from_list

from settings.driver import create_webdriver

# from engines.mountain_lion.download import execute_download
# from engines.mountain_lion.login import login
# from engines.mountain_lion.navigation import next_result
# from engines.mountain_lion.open_document import open_document
# from engines.mountain_lion.record import record
# from engines.mountain_lion.search import search


def execute_program(abstract):
    browser = create_webdriver(abstract)
    # login(browser, abstract)
    search_documents_from_list(
        browser,
        abstract,
        # search,
        # open_document,
        # record,
        # execute_download
        # next_result
    )
    close_program(browser, abstract)
