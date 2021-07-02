import os
from settings.file_management import strip_document_number_from_file_name

# The purposed of this script is to create hyperlinks for abstract exports
# it's "temporary" because the ideal situation will be to add hyperlinks directly into
# final product, but hit a roadblock which needs to be addressed later

# Note that this is creating a hyperlink for each file in the directory, rather than
# based on the document frame


def get_sorted_directory(directory):
    return sorted(os.listdir(directory))


def drop_ds_store(file):
    if file.endswith('.DS_Store'):
        os.remove(file)
        return True


def create_hyperlink_path(document_directory, file):
    return f'{document_directory}/{file}'


def create_hyperlink_cell(row):
    return f'A{str(row)}'


def write_hyperlink_url(document_directory, file, sheet, format, row):
    cell = create_hyperlink_cell(row)
    path = create_hyperlink_path(document_directory, file)
    name = strip_document_number_from_file_name(file)
    sheet.write_url(cell, path, format, name)


def write_temporary_hyperlinks(document_directory, sheet, format):
    row = 1
    for file in get_sorted_directory(document_directory):
        if not drop_ds_store(file):
            write_hyperlink_url(document_directory, file, sheet, format, row)
            row += 1
