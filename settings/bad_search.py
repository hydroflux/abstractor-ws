# Use the following print statement to identify the best way to manage imports for Django vs the script folder
print("bad_search", __name__)

from settings.file_management import (document_type, document_value,
                                      extrapolate_document_value)
from settings.settings import search_errors


def add_bad_search_key_values(dataframe, document):
    if document_type(document) == "document_number":
        document_number = document_value(document)
        dataframe["Book"].append(search_errors[2])
        dataframe["Page"].append(search_errors[2])
        dataframe["Reception Number"].append(document_number)
    elif document_type(document) == "book_and_page":
        book, page = document_value(document)
        dataframe["Book"].append(book)
        dataframe["Page"].append(page)
        dataframe["Reception Number"].append(search_errors[2])


def add_bad_search_message(dataframe, document):
    if document_type(document) == "document_number":
        document_number = document_value(document)
        bad_search_message = f'No document found at reception number {document_number}, please review'
    elif document_type(document) == "book_and_page":
        bad_search_message = f'No document found at {extrapolate_document_value(document)}, please review'
    dataframe["Comments"].append(bad_search_message)


def record_bad_search(dataframe, document):
    add_bad_search_key_values(dataframe, document)
    dataframe["Grantor"].append(search_errors[0])
    dataframe["Grantee"].append(search_errors[0])
    dataframe["Document Type"].append(search_errors[0])
    dataframe["Recording Date"].append(search_errors[1])
    dataframe["Legal"].append(search_errors[2])
    dataframe["Related Documents"].append(search_errors[2])
    add_bad_search_message(dataframe, document)


def no_document_image(dataframe, document):
    dataframe["Comments"][-1] = ('No document image located at '
                                 f'{extrapolate_document_value(document)}')
