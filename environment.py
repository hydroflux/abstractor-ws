from driver import chrome_webdriver
from execute import execute_script
from import_list import generate_document_list
from login import account_login
from variables import download_documents, file_name, sheet_name, target_directory, county
from user_prompts import continue_prompt, request_more_information
from export import export_document

def create_abstraction():
    document_list = generate_document_list(target_directory, file_name, sheet_name)
    browser = chrome_webdriver(target_directory)
    account_login(browser)
    abstract_dict = execute_script(browser, target_directory, document_list, download_documents)
    export_document(target_directory, file_name, abstract_dict)
    if continue_prompt(target_directory, file_name, sheet_name):
        document_list = request_more_information(target_directory, file_name, sheet_name)


def test():
    abstract_dict["Grantor"].append("Test")
    abstract_dict["Grantee"].append("Test")
    abstract_dict["Book"].append("Test")
    abstract_dict["Page"].append("Test")
    abstract_dict["Reception Number"].append("Test")
    abstract_dict["Document Type"].append("Test")
    abstract_dict["Recording Date"].append("Test")
    abstract_dict["Legal"].append("Test")
    abstract_dict["Related Documents"].append("Test")
    abstract_dict["Comments"].append("Test")
    return abstract_dict
