import os

# The purposed of this script is to create hyperlinks for abstract exports
# it's "temporary" because the ideal situation will be to add hyperlinks directly into
# final product, but hit a roadblock which needs to be addressed later


def get_sorted_directory(directory):
    return sorted(os.listdir(directory))


def drop_ds_store(file):
    if file.endswith('.DS_Store'):
        os.remove(file)
        return True


def create_hyperlink_path(document_directory, file):
    return f'{document_directory}/{file}'


def create_hyperlink_cell(row):
    return f'A{row}'


def create_hyperlink_name():
    pass


def write_hyperlink_url(document_directory, file, sheet, format, row):
    path = create_hyperlink_path(document_directory, file)
    cell = create_hyperlink_cell(row)
    name = create_hyperlink_name()
    sheet.write_url(cell, path, format, name)


def write_temporary_hyperlinks(document_directory, sheet, format):
    sorted_directory = get_sorted_directory(document_directory)
    for file in sorted_directory:
        row = 1
        if not drop_ds_store(file):
            write_hyperlink_url(document_directory, file, sheet, format, row)
            row += 1
