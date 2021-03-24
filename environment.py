from driver import chrome_webdriver
from execute import execute_program
from variables import county, download, file_name, sheet_name, target_directory

browser = chrome_webdriver(target_directory)
execute_program(browser, target_directory, file_name, sheet_name, download)
