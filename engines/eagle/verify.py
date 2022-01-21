# def get_first_result_value(browser, document):
#     first_result_info = get_first_result_info(browser)
#     if first_result_info is None:
#         return False
#     if document_type(document) == "document_number":
#         return first_result_info.text.split(" ")[0]
#     elif document_type(document) == "book_and_page":
#         try:
#             return get_book_and_page_values(browser, first_result_info)
#         except IndexError:
#             print(f'Encountered index error while splitting book & page for '
#                   f'{extrapolate_document_value(document)}, please review.')


# def verify_first_result_number(document, first_result_value):
#     if first_result_value == document_value(document):
#         return True
#     else:
#         print(f'First result Document number {first_result_value} does not match '
#               f'searched {extrapolate_document_value(document)}, please review.')
#         return False


# def verify_first_result_book_and_page(document, first_result_value):
#     if first_result_value is not False:
#         book = first_result_value[0]
#         page = first_result_value[1]
#         if book == document_value(document)[0] and page == document_value(document)[1]:
#             return True
#         else:
#             print(f'First result Book: {book}, Page: {page} does not match '
#                   f'searched {extrapolate_document_value(document)}, please review.')
#             return False
#     else:
#         return False


# Verify book & page is broken, need to assess verification on documents prior to 1900
# def verify_result(browser, document):
#     first_result_value = get_first_result_value(browser, document)
#     if first_result_value is False:
#         return False
#     if document_type(document) == "document_number":
#         return verify_first_result_number(document, first_result_value)
#     elif document_type(document) == "book_and_page":
#         # return verify_first_result_book_and_page(document, first_result_value)
#         return True


# def determine_document_status(browser, document):
#     if verify_result(browser, document):
#         print(f'{extrapolate_document_value(document)} matches the search result, moving forward.')
#         open_document_description(browser, get_first_result(browser))
#         naptime()
#         return True
#     else:
#         print(f'{extrapolate_document_value(document)} not found -- '
#               f'{get_first_result_value(browser, document)} returned as top search result.')
#         naptime()
#         return False
