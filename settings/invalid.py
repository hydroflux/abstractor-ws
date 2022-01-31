from settings.county_variables.general import search_errors
from settings.dataframe_management import no_document_downloaded, no_document_found

# Use the following print statement to identify the best way to manage imports for Django vs the script folder
print("bad_search", __name__)


def add_bad_search_key_values(dataframe, document):
    if document.type == "document_number":
        document_number = document.document_value()
        dataframe["Book"].append(search_errors[2])
        dataframe["Volume"].append(search_errors[2])
        dataframe["Page"].append(search_errors[2])
        dataframe["Reception Number"].append(document_number)
    elif document.type == "book_and_page":
        book, page = document.document_value()
        dataframe["Book"].append(book)
        dataframe["Volume"].append(search_errors[2])
        dataframe["Page"].append(page)
        dataframe["Reception Number"].append(search_errors[2])
    elif document.type == "volume_and_page":
        volume, page = document.document_value()
        dataframe["Book"].append(search_errors[2])
        dataframe["Volume"].append(volume)
        dataframe["Page"].append(page)
        dataframe["Reception Number"].append(search_errors[2])


def add_bad_search_message(dataframe, document):
    if document.type == "document_number":
        document_number = document.document_value()
        bad_search_message = f'No document located at reception number {document_number}, please review'
    elif document.type == "book_and_page" or document.type == "volume_and_page":
        bad_search_message = f'No document located at {document.extrapolate_value()}, please review'
    dataframe["Comments"].append(bad_search_message)


def record_invalid_search(abstract, document):
    if not abstract.download_only:
        add_bad_search_key_values(abstract.dataframe, document)
        abstract.dataframe["Grantor"].append(search_errors[0])
        abstract.dataframe["Grantee"].append(search_errors[0])
        abstract.dataframe["Document Type"].append(search_errors[0])
        abstract.dataframe["Document Link"].append(search_errors[-2])
        abstract.dataframe["Effective Date"].append(search_errors[-2])
        abstract.dataframe["Recording Date"].append(search_errors[1])
        abstract.dataframe["Legal"].append(search_errors[-2])
        abstract.dataframe["Related Documents"].append(search_errors[-2])
        add_bad_search_message(abstract.dataframe, document)
    no_document_found(abstract, document)


def unable_to_download(abstract, document):
    last_comment = abstract.dataframe["Comments"][-1]
    unable_to_download = f'Unable to download document image at {document.extrapolate_value()}, please review'
    if last_comment == "":
        abstract.dataframe["Comments"][-1] = unable_to_download
    else:
        abstract.dataframe["Comments"][-1] = f'{last_comment}; {unable_to_download}'


def no_document_image(abstract, document):
    last_comment = abstract.dataframe["Comments"][-1]
    no_image_comment = (f'No document image available for '
                        f'"{document.extrapolate_value()}", please review')
    print(no_image_comment)
    if last_comment == "":
        abstract.dataframe["Comments"][-1] = no_image_comment
    else:
        abstract.dataframe["Comments"][-1] = f'{last_comment}; {no_image_comment}'


def no_download(abstract, document):
    unable_to_download(abstract, document)
    no_document_downloaded(abstract, document)
