from driver import chrome_webdriver
from import_list import generate_document_list
from execute import execute_script

from variables import target_directory, file_name, sheet_name

document_list = generate_document_list(target_directory, file_name, sheet_name)
browser = chrome_webdriver(target_directory)
abstract_dataframe = execute_script(browser, document_list)


document_number = "4467371"