from driver import chrome_webdriver
from login import account_login
from search import document_number_search
from open import open_document
# from record import 
from download import download_document

from variables import target_directory

browser = chrome_webdriver(target_directory)
account_login(browser)

# for x in y
document_number_search(browser, document_number)
if open_document(browser, document_number):
    # record
    download_document(browser)
else:
    print("No document found")
    # record_bad_search