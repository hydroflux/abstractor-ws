from driver import chrome_webdriver
from execute import execute_script
from import_list import generate_document_list
from login import account_login
from variables import download_documents, file_name, sheet_name, target_directory, county
from user_prompts import continue_prompt, request_more_information


def create_abstraction():
    document_list = generate_document_list(target_directory, file_name, sheet_name)
    browser = chrome_webdriver(target_directory)
    account_login(browser)
    abstract_dataframe = execute_script(browser, target_directory, document_list, download_documents)
    if continue_prompt(target_directory, file_name, sheet_name):
        document_list = request_more_information(target_directory, file_name, sheet_name)
