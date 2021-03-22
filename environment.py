from driver import chrome_webdriver
from import_list import generate_document_list
from login import account_login
from search import document_number_search
from open_site import open_document
from record import record_document, record_bad_search
from download import download_document
from dataframe import abstract_dataframe

from variables import target_directory, file_name, sheet_name

browser = chrome_webdriver(target_directory)
account_login(browser)
document_list = generate_document_list(target_directory, file_name, sheet_name)

for document_number in document_list:
    document_number_search(browser, document_number)
    if open_document(browser, document_number):
        record_document(browser, abstract_dataframe, document_number)
        download_document(browser)
    else:
        record_bad_search(dataframe, document_number)