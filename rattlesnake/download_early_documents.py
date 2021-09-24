from rattlesnake.search import clear_search
from selenium_utilities.open import open_url


from rattlesnake.rattlesnake_variables import old_search_url, old_search_title


# def handle_search_years(browser, document):
#     if document.year < '1985' and document.year != '1700':
#         enter_input_value(browser, locate_input, document.input_ids["Date Start"],
#                           "Date Start Input", f'01/01/{document.year}', document)
#         enter_input_value(browser, locate_input, document.input_ids["Date End"],
#                           "Date Start Input", f'12/31/{document.year}', document)
#         click_button(browser, locate_input, document.input_ids["Volume"],
#                      "Volume Input", document)


def open_early_documents(browser):
    open_url(browser, old_search_url, old_search_title, "old document search")
    clear_search(browser, document)
    handle_document_value_numbers(browser, document)  # Enter Value Numbers
    click_button(browser, locate_input, document.button_ids["Submit Button"],
                    "submit button", document)  # Execute Search