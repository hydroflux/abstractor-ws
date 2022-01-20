import os

if __name__ == '__main__':
    from settings.general_functions import four_character_padding, report_execution_time
else:
    from .general_functions import four_character_padding, report_execution_time


def remaining_documents(document_list, document):
    return len(document_list) - document_list.index(document) - 1


def list_remaining_documents(document_list, document):
    return f'{remaining_documents(document_list, document)} documents remaining'


def multiple_documents_comment(document):
    return (f'Multiple documents located at {document.extrapolate_value()}'
            f' on the {document.county} recording website; Each of the {document.number_results}'
            f' documents has been listed, please review')


# def document_value(document):
#     if document.type == "document_number" or document.type == "name":
#         return str(document.value)
#     elif document.type == "book_and_page":
#         return [str(document.value["Book"]), str(document.value["Page"])]
#     elif document.type == "volume_and_page":
#         return [str(document.value["Volume"]), str(document.value["Page"])]
#     else:
#         print('Unable to identify document type while attempting to identify "document value", please review.')
#         return None


# def extrapolate_document_value(document):
#     value = document.document_value()
#     if document.type == "book_and_page":
#         return f'Book: {value[0]}, Page: {value[1]}'
#     elif document.type == "volume_and_page":
#         return f'Volume: {value[0]}, Page: {value[1]}'
#     elif document.type == "document_number":
#         return f'Document number {value}'
#     elif document.type == "name":
#         return f'search name "{value}"'
#     else:
#         print('Unable to identify document type while attempting to "extrapolate document value", please review.')
#         return None


# Consolidate split_book_and_page & split_volume_and_page
def split_book_and_page(document):
    book = four_character_padding(document.document_value()[0])
    page = four_character_padding(document.document_value()[1])
    return book, page
    # Check to see if the padding is affecting search results
    # Consider only adding the padding when updating the document frame


# This function isn't necessary, just split instead of call
def split_volume_and_page(document):
    volume = document.document_value()[0]
    page = document.document_value()[1]
    return volume, page


# def drop_last_entry(dataframe):
#     dataframe["Grantor"].pop()
#     dataframe["Grantee"].pop()
#     dataframe["Book"].pop()
#     dataframe["Volume"].pop()
#     dataframe["Page"].pop()
#     dataframe["Reception Number"].pop()
#     dataframe["Document Link"].pop()
#     dataframe["Document Type"].pop()
#     dataframe["Effective Date"].pop()
#     dataframe["Recording Date"].pop()
#     dataframe["Legal"].pop()
#     dataframe["Related Documents"].pop()
#     dataframe["Comments"].pop()


# def check_last_document(dataframe, document_list, document):
#     if len(dataframe['Reception Number']) >= 2:
#         if document.index_number == document_list[document_list.index(document) - 1].index_number and \
#           document.result_number == 0:
#             if dataframe["Grantor"][-1] == dataframe["Grantor"][-2] and \
#               dataframe["Grantee"][-1] == dataframe["Grantee"][-2] and \
#               dataframe["Book"][-1] == dataframe["Book"][-2] and \
#               dataframe["Volume"][-1] == dataframe["Volume"][-2] and \
#               dataframe["Page"][-1] == dataframe["Page"][-2] and \
#               dataframe["Reception Number"][-1] == dataframe["Reception Number"][-2] and \
#               dataframe["Document Link"][-1] == dataframe["Document Link"][-2] and \
#               dataframe["Document Type"][-1] == dataframe["Document Type"][-2] and \
#               dataframe["Effective Date"][-1] == dataframe["Effective Date"][-2] and \
#               dataframe["Recording Date"][-1] == dataframe["Recording Date"][-2] and \
#               dataframe["Legal"][-1] == dataframe["Legal"][-2] and \
#               dataframe["Related Documents"][-1] == dataframe["Related Documents"][-2] and \
#               dataframe["Comments"][-1] == dataframe["Comments"][-2]:
#                 drop_last_entry(dataframe)


# def check_length(dataframe):
#     grantors = len(dataframe["Grantor"])
#     grantees = len(dataframe["Grantee"])
#     books = len(dataframe["Book"])
#     volumes = len(dataframe["Volume"])
#     pages = len(dataframe["Page"])
#     reception_numbers = len(dataframe["Reception Number"])
#     document_links = len(dataframe["Document Link"])
#     document_types = len(dataframe["Document Type"])
#     effective_dates = len(dataframe["Effective Date"])
#     recording_dates = len(dataframe["Recording Date"])
#     legals = len(dataframe["Legal"])
#     related_documents = len(dataframe["Related Documents"])
#     comments = len(dataframe["Comments"])
#     if (grantors == grantees == books == volumes == pages
#             == reception_numbers == document_links == document_types
#             == effective_dates == recording_dates == legals
#             == related_documents == comments):
#         pass
#     else:
#         print("Grantors: ", grantors)
#         print("Grantees: ", grantees)
#         print("Books: ", books)
#         print("Volumes: ", volumes)
#         print("Pages: ", pages)
#         print("Reception Numbers: ", reception_numbers)
#         print("Document Links: ", document_links)
#         print("Document Types: ", document_types)
#         print("Effective Dates: ", effective_dates)
#         print("Recording Dates: ", recording_dates)
#         print("Legals: ", legals)
#         print("Related Documents: ", related_documents)
#         print("Comments: ", comments)


def account_for_number_results(document):
    if document.number_results > 1:
        return f' - {document.number_results} results found for {document.extrapolate_value()}'
    else:
        return ''


def document_found(abstract, document):
    if abstract.review is False:
        print('Document located at '
              f'{document.extrapolate_value()} recorded'
              f'{account_for_number_results(document)}, '
              f'{list_remaining_documents(abstract.document_list, document)} '
              f'({report_execution_time(document.start_time)})')
    elif abstract.review is True:
        input(f'Document located at {document.extrapolate_value()} found'
              f'{account_for_number_results(document)}, '
              'please review & press enter to continue... '
              f'({list_remaining_documents(abstract.document_list, document)}) '
              f'({report_execution_time(document.start_time)})')
    # elif alt == "download":
    #     print('Document located at '
    #           f'{document.extrapolate_value()} downloaded, '
    #           f'{list_remaining_documents(document_list, document)} '
    #           f'({report_execution_time(start_time)})')


def no_document_found(abstract, document):
    if abstract.review is False:
        print('No document found at '
              f'{document.extrapolate_value()}, '
              f'{list_remaining_documents(abstract.document_list, document)} '
              f'({report_execution_time(document.start_time)})')
    elif abstract.review is True:
        input(f'No document found at {document.extrapolate_value()}, '
              'please review & press enter to continue... '
              f'({list_remaining_documents(abstract.document_list, document)}) '
              f'({report_execution_time(document.start_time)})')


def document_downloaded(document_list, document, download_only=False):
    print(f'Document located at '
          f'{document.extrapolate_value()} downloaded'
          f'{account_for_number_results(document)}, '
          f'{list_remaining_documents(document_list, document)} '
          f'{"(" + (report_execution_time(document.start_time)) + ")" if download_only else ""}')


def no_document_downloaded(document_list, document, download_only=False):
    print(f'Unable to download document at '
          f'{document.extrapolate_value()}'
          f'{account_for_number_results(document)}, '
          f'({list_remaining_documents(document_list, document)}) '
          f'{"(" + (report_execution_time(document.start_time)) + ")" if download_only else ""}')


def rename_documents_in_directory(county, directory):
    os.chdir(directory)
    for pdf in os.listdir(directory):
        if pdf == '.DS_Store':
            full_path = os.path.join(directory, pdf)
            os.remove(full_path)
        elif pdf.startswith(county.prefix):
            continue
        else:
            new_document_name = county.prefix + '-' + pdf
            full_path = os.path.join(directory, pdf)
            os.rename(full_path, new_document_name)
            size = os.stat(new_document_name) == 0
            if size is True:
                os.remove(new_document_name)
                print('Failed to download reception number ' + pdf)


def remove_prefix(string, prefix):
    return string[(string.find(prefix) + 1):]


def remove_file_suffix(file_name):
    return file_name[:file_name.rfind(".")]


def strip_document_number_from_file_name(file_name):
    return remove_file_suffix(remove_prefix(file_name, "-"))


def clear_dictionary(dictionary):
    [dictionary[key].clear() for key in dictionary]


def last_document(document_list, document):
    return document_list[document_list.index(document) - 1]
