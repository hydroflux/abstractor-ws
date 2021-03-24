import os

import pandas as pd
import xlsxwriter

from variables import abstraction_type, authorship, worksheet_properties, text_formats, header_content


def prepare_output_environment(target_directory):
    os.chdir(target_directory)


def create_output_file(file_name):
    abstraction_export = '-'.join(abstraction_type.upper().split(' '))
    return f'{file_name}-{abstraction_export}'


def create_excel_writer(output_file):
    return pd.ExcelWriter(output_file, engine='xlsxwriter', datetime_format='mm/dd/yyyy', date_format='mm/dd/yyyy')  # pylint: disable=abstract-class-instantiated


def add_column(dataframe, column):
    dataframe.insert(column.position, column.title, '')


def add_breakpoints(dataframe):
    current_position = dataframe.columns.get_loc(worksheet_properties['breakpoint_start'])
    for column in worksheet_properties['breakpoints']:
        column.position = current_position + current_position
        add_column(dataframe, column)


def create_excel_object(writer, dataframe, sheet_name):
    add_breakpoints(dataframe)
    return dataframe.to_excel(
        writer,
        sheet_name=sheet_name,
        startrow=worksheet_properties['startrow'],
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


def set_workbook_properties(workbook):
    workbook.set_properties(authorship)


def set_font_formats(workbook):
    return {
        'large': workbook.add_format(text_formats['large']),
        'small': workbook.add_format(text_formats['small']),
        'header': workbook.add_format(text_formats['header']),
        'datatype': workbook.add_format(text_formats['datatype']),
        'body': workbook.add_format(text_formats['body']),
        # 'border': workbook.add_format(text_formats['border'])
        'footer_title': workbook.add_format(text_formats['footer_title']),
        'footer': workbook.add_format(text_formats['footer']),
    }
    

def format_workbook(writer):
    workbook = access_workbook_object(writer)
    set_workbook_properties(workbook)
    return set_font_formats(workbook)


def set_page_format(worksheet):
    worksheet.set_landscape()
    worksheet.set_paper(worksheet_properties['paper_type'])
    worksheet.set_margins(left=0.25, right=0.25, top=0.75, bottom=0.75)
    worksheet.hide_gridlines(worksheet_properties['gridlines'])


def set_title_format(worksheet):
    worksheet.set_row(0, worksheet_properties['header_height'])


def create_range_message(dataframe, content):
    return f'From {dataframe[breakpoint_start].iloc[0]} to \
        {dataframe[breakpoint_start].iloc[-1]} \n \
        ({content['order']})'


def write_title_content(dataframe, worksheet, font_formats):
    content = worksheet_properties['header_content']
    range_message = create_range_message(dataframe, content)
    worksheet.write_rich_string(
        'A1',
        font_formats['large'], content['type'],
        font_formats['large'], content['user'],
        font_formats['small'], content['scope'],
        font_formats['small'], content['county'],
        font_formats['small'], range_message,
        font_formats['header']
        )


def add_title_row(dataframe, worksheet, font_formats):
    set_title_format(worksheet)
    write_title_content(dataframe, worksheet, font_formats)


def number_to_letter(number):
    return chr(ord('@')+(number))


def merge_primary_datatype_ranges(dataframe, font_format):
    primary_range = worksheet_properties['datatype_content']['primary_datatype_columns']
    for column in primary_range:
        column_name = dataframe.columns[column] 
        column_position = number_to_letter((column + 1))
        worksheet.merge_range(
            f'{column_position}2:{column_position}3',
            column_name,
            font_format
            )


def merge_custom_column(dataframe, font_format):
    custom_column = worksheet_properties['datatype_content']['custom_datatype_column']
    column_name = dataframe.columns[custom_column] 
    column_position_start = number_to_letter((column + 1))
    column_position_end = number_to_letter((column + 4))
    worksheet.merge_range(
        f'{column_position_start}2:{column_position_end}2',
        column_name,
        font_format
        )


def merge_secondary_datatype_ranges(dataframe, font_format):
    primary_range = worksheet_properties['datatype_content']['secondary_datatype_columns']
    for column in primary_range:
        column_name = dataframe.columns[column] 
        column_position = number_to_letter((column + 1))
        worksheet.merge_range(
            f'{column_position}3',
            column_name,
            font_format
            )


def add_dataframe_headers(dataframe, worksheet, font_format):
    merge_primary_datatype_ranges(dataframe, font_format)
    merge_custom_datatype_range(dataframe, font_format)
    merge_secondary_datatype_ranges(dataframe, font_format)


def set_column_formats(worksheet, font_format):
    for column in worksheet_properties['column_formats']:
        worksheet.set_column(column.column_range, column.width, font_format)


def count_columns(dataframe):
    return len(dataframe.columns)

def access_last_row(dataframe):
    return len(dataframe.index) + worksheet_properties['startrow']

# def set_worksheet_border(dataframe):
#     number_columns = count_columns(dataframe)
#     last_row = access_last_row(dataframe)
#     main_content_range = f'A3:{number_to_letter(number_columns)}{last_row}'

def set_footer_title(worksheet, last_column, last_row, font_format):
    footer_title_row = last_row + 1
    footer_title_range = f'A{footer_title_row}:{last_column}{footer_title_row}'
    worksheet.set_row(last_row, worksheet_properties['footer_title_height'])
    worksheet.merge_range(footer_title_range, worksheet_properties['footer_title_content'], font_format)


def set_footer(worksheet, last_column, last_row, font_format):
    footer_row = last_row + 2
    footer_range = f'A{footer_row}:{last_column}{footer_row}'
    worksheet.set_row((footer_row - 1), worksheet_properties['footer-height'])
    worksheet.merge_range(footer_title_range, worksheet_properties['footer-content'], font_format)


def add_footer_row(dataframe, worksheet, font_formats):
    last_column = number_to_letter(count_columns(dataframe))
    last_row = access_last_row(dataframe)
    set_footer_title(worksheet, last_column, last_row, font_formats['footer'])
    set_footer(worksheet, last_column, last_row, font_format)


def format_worksheet(dataframe, worksheet, font_formats):
    set_page_format(worksheet)
    add_title_row(dataframe, worksheet, font_formats)
    add_dataframe_headers(dataframe, font_formats['datatype'])
    set_column_formats(worksheet, font_formats['body'])
    # set_worksheet_border(dataframe)
    add_footer_row(dataframe, worksheet, font_formats)


def format_xlsx_worksheet(writer, dataframe, font_formats):
    worksheet = access_worksheet_object(writer)
    format_worksheet(dataframe, worksheet, font_formats)


def format_xlsx_document(writer, dataframe):
    font_formats = format_workbook(writer)
    format_worksheet(writer, dataframe, font_formats)


def close_workbook(workbook):
    workbook.close()


def save_xlsx_document(writer):
    writer.save()


def finalize_xlsx_document(writer, dataframe):
    format_xlsx_document(writer, dataframe)
    save_xlsx_document(writer)


def export_document(target_directory, file_name, dataframe):
    prepare_output_environment(target_directory)
    writer = create_xlsx_document(file_name, dataframe)
    finalize_xlsx_document(writer, dataframe)
