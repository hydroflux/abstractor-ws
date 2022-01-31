import os
from settings.dataframe_management import strip_document_number_from_file_name

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


def create_hyperlink_cell(row):
    return f'A{str(row)}'


def get_current_folder_name():
    return os.getcwd().split('/')[-1]


def create_hyperlink_path(file):
    return f'{get_current_folder_name()}/{file}'


def write_hyperlink_url(directory, file, sheet, format):
    row = directory.index(file) + 1
    cell = create_hyperlink_cell(row)
    path = create_hyperlink_path(file)
    name = strip_document_number_from_file_name(file)
    sheet.write_url(cell, path, format, name)


def write_temporary_hyperlinks(document_directory, sheet, format):
    os.chdir(document_directory)
    directory = get_sorted_directory(document_directory)
    for file in directory:
        if not drop_ds_store(file):
            write_hyperlink_url(directory, file, sheet, format)


#####################################################################


def create_hyperlink_sheet(project):
    hyperlink_sheet = project.workbook.add_worksheet("Hyperlink")
    hyperlink_sheet.set_column('A:A', 20)
    return hyperlink_sheet


def add_hyperlink_sheet(abstract, project):
    if abstract.download:
        hyperlink_format = project.workbook.add_format(project.text_formats['hyperlink'])
        hyperlink_sheet = create_hyperlink_sheet(project)
        write_temporary_hyperlinks(abstract.document_directory, hyperlink_sheet, hyperlink_format)
        os.chdir(abstract.target_directory)  # Is this necessary?


# def export_hyperlinks(abstract):
#     os.chdir(abstract.target_directory)
#     output_file, writer = create_xlsx_document(abstract.target_directory, abstract.file_name, abstract.dataframe)
#     workbook = access_workbook_object(writer)
#     add_hyperlink_sheet(abstract, workbook)
#     workbook.close()
#     return output_file
