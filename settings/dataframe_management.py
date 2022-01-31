import os


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
