import os

if __name__ == '__main__':
    from settings.general_functions import report_execution_time
else:
    from .general_functions import report_execution_time


def multiple_documents_comment(document):
    return (f'Multiple documents located at {document.extrapolate_value()}'
            f' on the {document.county} recording website; Each of the {document.number_results}'
            f' documents has been listed, please review')


# # Consolidate split_book_and_page & split_volume_and_page
# def split_book_and_page(document):
#     book = four_character_padding(document.document_value()[0])
#     page = four_character_padding(document.document_value()[1])
#     return book, page
#     # Check to see if the padding is affecting search results
#     # Consider only adding the padding when updating the document frame


# This function isn't necessary, just split instead of call
# def split_volume_and_page(document):
#     volume = document.document_value()[0]
#     page = document.document_value()[1]
#     return volume, page


def account_for_number_results(document):
    if document.number_results > 1:
        return f' - {document.number_results} results found for {document.extrapolate_value()}'
    else:
        return ''


def remaining_documents(document_list, document):
    return len(document_list) - document_list.index(document) - 1


def list_remaining_documents(document_list, document):
    return f'{remaining_documents(document_list, document)} documents remaining'


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


def document_downloaded(abstract, document):
    print(f'Document located at '
          f'{document.extrapolate_value()} downloaded'
          f'{account_for_number_results(document)}, '
          f'{list_remaining_documents(abstract.document_list, document)} '
          f'{"(" + (report_execution_time(document.start_time)) + ")" if abstract.download_only else ""}')


def no_document_downloaded(abstract, document):
    print(f'Unable to download document at '
          f'{document.extrapolate_value()}'
          f'{account_for_number_results(document)}, '
          f'({list_remaining_documents(abstract.document_list, document)}) '
          f'{"(" + (report_execution_time(document.start_time)) + ")" if abstract.download_only else ""}')


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
