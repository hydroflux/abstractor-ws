from engines.mountain_lion.iframe_handling import switch_to_main_frame
from settings.general_functions import javascript_script_execution


def handle_disclaimer(browser, abstract):
    switch_to_main_frame(browser, abstract)
    javascript_script_execution(browser, abstract.county.scripts['Disclaimer'])
