import os
import shutil

from settings.settings import download

if __name__ == '__main__':
    from settings.general_functions import four_character_padding, report_execution_time
else:
    from .general_functions import four_character_padding, report_execution_time


def create_folder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory ' + directory)


def document_directory_exists(target_directory):
    if os.path.exists(f'{target_directory}/Documents'):
        return True


def access_document_directory(target_directory):
    return f'{target_directory}/Documents'


def create_document_directory(target_directory):
    document_directory = access_document_directory(target_directory)
    create_folder(document_directory)
    os.chdir(document_directory)
    return document_directory


def remaining_documents(document_list, document):
    return len(document_list) - document_list.index(document) - 1


def list_remaining_documents(document_list, document):
    return f'{remaining_documents(document_list, document)} documents remaining'


def multiple_documents_comment(county, document):
    return (f'Multiple documents located at {extrapolate_document_value(document)}'
            f' on the {county} recording website; Each of the {document.number_results}'
            f' documents has been listed, please review')


def document_type(document):
    return str(document.type)


def document_value(document):
    if document_type(document) == "document_number" or document_type(document) == "name":
        return str(document.value)
    elif document_type(document) == "book_and_page":
        return [str(document.value["Book"]), str(document.value["Page"])]


def extrapolate_document_value(document):
    value = document_value(document)
    type = document_type(document)
    if type == "book_and_page":
        return f'Book: {value[0]}, Page: {value[1]}'
    elif type == "document_number":
        return f'Document number {value}'
    elif type == "name":
        return f'search name "{value}"'


def split_book_and_page(document):
    book = four_character_padding(document_value(document)[0])
    page = four_character_padding(document_value(document)[1])
    return book, page
    # Check to see if the padding is affecting search results
    # Consider only adding the padding when updating the document frame


def display_document_list(document_list):
    print(f'{len(document_list)} documents to be recorded:')
    for document in range(len(document_list)):
        print(document_value(document_list[document]))
    print()


def drop_last_entry(dataframe):
    dataframe["Grantor"].pop()
    dataframe["Grantee"].pop()
    dataframe["Book"].pop()
    dataframe["Page"].pop()
    dataframe["Reception Number"].pop()
    dataframe["Document Type"].pop()
    dataframe["Recording Date"].pop()
    dataframe["Legal"].pop()
    dataframe["Related Documents"].pop()
    dataframe["Comments"].pop()


def check_length(dataframe):
    grantors = len(dataframe["Grantor"])
    grantees = len(dataframe["Grantee"])
    books = len(dataframe["Book"])
    pages = len(dataframe["Page"])
    reception_numbers = len(dataframe["Reception Number"])
    document_types = len(dataframe["Document Type"])
    recording_dates = len(dataframe["Recording Date"])
    legals = len(dataframe["Legal"])
    related_documents = len(dataframe["Related Documents"])
    comments = len(dataframe["Comments"])
    if (grantors == grantees == books == pages
            == reception_numbers == document_types
            == recording_dates == legals == related_documents
            == comments):
        pass
    else:
        print("Grantors: ", grantors)
        print("Grantees: ", grantees)
        print("Books: ", books)
        print("Pages: ", pages)
        print("Reception Numbers: ", reception_numbers)
        print("Document Types: ", document_types)
        print("Recording Dates: ", recording_dates)
        print("Legals: ", legals)
        print("Related Documents: ", related_documents)
        print("Comments: ", comments)


def document_found(start_time, document_list, document, alt=None):
    if alt is None:
        print('Document located at '
              f'{extrapolate_document_value(document)} recorded, '
              f'{list_remaining_documents(document_list, document)} '
              f'({report_execution_time(start_time)})')
    elif alt == "review":
        input(f'Document located at {extrapolate_document_value(document)} found,'
              'please review & press enter to continue... '
              f'({list_remaining_documents(document_list, document)}) '
              f'({report_execution_time(start_time)})')
    elif alt == "download":
        print('Document located at '
              f'{extrapolate_document_value(document)} downloaded, '
              f'{list_remaining_documents(document_list, document)} '
              f'({report_execution_time(start_time)})')


def no_document_found(start_time, document_list, document, alt=None):
    if alt is None:
        print('No document found at '
              f'{extrapolate_document_value(document)}, '
              f'{list_remaining_documents(document_list, document)} '
              f'({report_execution_time(start_time)})')
    elif alt == "review":
        input(f'No document found at {extrapolate_document_value(document)}, '
              'please review & press enter to continue... '
              f'({list_remaining_documents(document_list, document)}) '
              f'({report_execution_time(start_time)})')


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


def create_project_folder(target_directory, abstraction):
    project_folder = f'{target_directory}/{abstraction[:-5]}'
    create_folder(project_folder)
    return project_folder


def move_abstraction_into_project_folder(target_directory, project_folder, abstraction):
    # shutil.move(f'{target_directory}/{file_name}-{abstraction_type.upper()}.xlsx', project_folder)
    shutil.move(f'{target_directory}/{abstraction}', project_folder)


def move_downloaded_documents(target_directory, project_folder):
    if download:
        shutil.move(f'{target_directory}/Documents', project_folder)


def bundle_project(target_directory, abstraction):
    os.chdir(target_directory)
    project_folder = create_project_folder(target_directory, abstraction)
    move_abstraction_into_project_folder(target_directory, project_folder, abstraction)
    move_downloaded_documents(target_directory, project_folder)
    # shutil.move(f'{target_directory}/{file_name}.xlsx', project_folder)
