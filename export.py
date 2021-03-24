import pandas as pd
import os
import xlsxwriter

from variables import abstraction_type

# def import_excel_document(file_path, sheet_name):
#     excel = pd.read_excel(file_path, sheet_name)
#     int_document_list = excel.values.flatten().tolist()
#     return [str(i) for i in int_document_list]

# def generate_document_list(target_directory, file_name, sheet_name):
#     file_path = f'{target_directory}/{file_name}.xlsx'
#     return import_excel_document(file_path, sheet_name)

# def export_excel_document(target_directory, file_name, dataframe):
#     os.chdir(target_directory)
#     output_file = create_output_file(file_name)
#     dataframe.to_excel(f'{output_file}.xlsx')

def prepare_output_environment(target_directory):
    os.chdir(target_directory)


def create_output_file(file_name):
    abstraction_export = '-'.join(abstraction_type.upper().split(' '))
    return f'{file_name}-{abstraction_export}'


def create_excel_writer(output_file):
    return pd.ExcelWriter(output_file, engine='xlsxwriter', datetime_format='mm/dd/yyyy', date_format='mm/dd/yyyy')  # pylint: disable=abstract-class-instantiated


def create_excel_object(writer, dataframe, sheet_name):
    return dataframe.to_excel(
        writer,
        sheet_name=sheet_name,
        startrow=3,
        header=False,
        index=False
        )


def create_xlsx_document(file_name, dataframe):
    output_file = create_output_file(file_name)
    writer = create_excel_writer(output_file)
    create_excel_object(writer, dataframe, abstraction_type)
    return writer


def access_workbook_object(writer):
    return writer.book


def access_worksheet_object(writer):
    return writer.sheets


def format_workbook():
    pass


def format_worksheet():
    pass


def format_xlsx_document(writer):
    workbook = access_workbook_object(writer)
    worksheet = access_worksheet_object(writer)
    format_worksheet(worksheet)


def save_xlsx_document(writer):
    writer.save()


def finalize_xlsx_document(writer):
    format_xlsx_document(writer)
    save_xlsx_document(writer)


def export_document(target_directory, file_name, dataframe):
    prepare_output_environment(target_directory)
    writer = create_xlsx_document(file_name, dataframe)
    finalize_xlsx_document(writer)