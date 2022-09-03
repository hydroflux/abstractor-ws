from engines.platypus.collect import collect
from settings.general_functions import javascript_script_execution


def open_document(browser, abstract, document):
    if not document.description_link or document.result_number > 0:
        collect(browser, abstract, document)
    javascript_script_execution(browser, document.description_link)
    return True
