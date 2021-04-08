import os

from pandas import DataFrame, ExcelWriter
import xlsxwriter

if __name__ == '__main__':
    from settings.settings import (abstraction_type, authorship, text_formats,
                                   worksheet_properties)
else:
    from .settings import (abstraction_type, authorship, text_formats,
                           worksheet_properties)


def prepare_output_environment(target_directory):
    os.chdir(target_directory)


def create_dataframe(dictionary):
    dataframe = DataFrame(dictionary)
    print(dataframe)


def transform_dictionary(dictionary):
    dataframe = create_dataframe(dictionary)
    dataframe.rename({"Legal": "Legal Description"}, axis=1)
    return dataframe


def create_output_file(file_name):
    abstraction_export = '-'.join(abstraction_type.upper().split(' '))
    return f'{file_name}-{abstraction_export}.xlsx'


def create_excel_writer(output_file):
    return ExcelWriter(
        output_file,
        engine='xlsxwriter',
        datetime_format='mm/dd/yyyy',
        date_format='mm/dd/yyyy')  # pylint: disable=abstract-class-instantiated


def add_column(dataframe, current_position, column):
    dataframe.insert(current_position, column.title, '')


def add_breakpoints(dataframe):
    current_position = dataframe.columns.get_loc(worksheet_properties['breakpoint_start'])
    for column in worksheet_properties['breakpoints']:
        add_column(dataframe, current_position, column)
        current_position = current_position + column.position


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
    create_excel_object(writer, dataframe, abstraction_type.upper())
    return writer


def access_workbook_object(writer):
    return writer.book


def access_worksheet_object(writer):
    return writer.sheets[(abstraction_type.upper())]


def set_workbook_properties(workbook):
    workbook.set_properties(authorship)


def set_font_formats(workbook):
    return {
        'large': workbook.add_format(text_formats['large']),
        'small': workbook.add_format(text_formats['small']),
        'header': workbook.add_format(text_formats['header']),
        'datatype': workbook.add_format(text_formats['datatype']),
        'body': workbook.add_format(text_formats['body']),
        'border': workbook.add_format(text_formats['border']),
        'footer_title': workbook.add_format(text_formats['footer_title']),
        'footer': workbook.add_format(text_formats['footer']),
    }


def format_workbook(writer):
    workbook = access_workbook_object(writer)
    set_workbook_properties(workbook)
    return set_font_formats(workbook), workbook


def set_page_format(worksheet):
    worksheet.set_landscape()
    worksheet.set_paper(worksheet_properties['paper_size'])
    worksheet.set_margins(left=0.25, right=0.25, top=0.75, bottom=0.75)
    worksheet.hide_gridlines(worksheet_properties['gridlines'])
    worksheet.freeze_panes(f'A{worksheet_properties["startrow"] + 1}')


def format_worksheet(writer):
    worksheet = access_worksheet_object(writer)
    set_page_format(worksheet)
    return worksheet


def count_columns(dataframe):
    return len(dataframe.columns)


def number_to_letter(number):
    return chr(ord('@') + (number))


def set_title_format(dataframe, worksheet, font_format):
    worksheet.set_row(0, worksheet_properties['header_height'])
    worksheet.merge_range(f'A1:{number_to_letter(count_columns(dataframe))}1', '', font_format)


def create_range_message(dataframe, content):
    start = dataframe[worksheet_properties["breakpoint_start"]]
    return f'From {start.iloc[0]} to {start.iloc[-1]} \n ({content["order"]})'


def write_title_content(dataframe, worksheet, font_formats, client=None, legal=None):
    content = worksheet_properties['header_content']
    range_message = create_range_message(dataframe, content)
    if client is not None and legal is not None:
        content['user'] = f'{client}\n'
        content['scope'] = f'{legal}\n'
    worksheet.write_rich_string(
        'A1',
        font_formats['large'], content['type'],
        font_formats['large'], content['user'],
        font_formats['small'], content['scope'],
        font_formats['small'], content['county'],
        font_formats['small'], range_message,
        font_formats['header']
    )


def add_title_row(dataframe, worksheet, font_formats, client=None, legal=None):
    set_title_format(dataframe, worksheet, font_formats['header'])
    write_title_content(dataframe, worksheet, font_formats, client, legal)


def merge_primary_datatype_ranges(dataframe, worksheet, font_format):
    primary_range = worksheet_properties['datatype_content']['primary_datatype_columns']
    for column in primary_range:
        column_name = dataframe.columns[column]
        column_position = number_to_letter((column + 1))
        worksheet.merge_range(
            f'{column_position}2:{column_position}3',
            column_name,
            font_format
        )


def merge_custom_column(dataframe, worksheet, font_format):
    column = worksheet_properties['datatype_content']['custom_datatype_column']
    column_position_start = number_to_letter((column + 1))
    column_position_end = number_to_letter((column + 4))
    worksheet.merge_range(
        f'{column_position_start}2:{column_position_end}2',
        worksheet_properties['custom_column_name'],
        font_format
    )


def merge_secondary_datatype_ranges(dataframe, worksheet, font_format):
    primary_range = worksheet_properties['datatype_content']['secondary_datatype_columns']
    for column in primary_range:
        column_name = dataframe.columns[column]
        column_position = number_to_letter((column + 1))
        worksheet.write(
            f'{column_position}3',
            column_name,
            font_format
        )


def add_dataframe_headers(dataframe, worksheet, font_format):
    merge_primary_datatype_ranges(dataframe, worksheet, font_format)
    merge_custom_column(dataframe, worksheet, font_format)
    merge_secondary_datatype_ranges(dataframe, worksheet, font_format)


def access_last_row(dataframe):
    return len(dataframe.index) + worksheet_properties['startrow']


def set_worksheet_border(dataframe, worksheet, font_format):
    number_columns = count_columns(dataframe)
    worksheet_range = f'A{worksheet_properties["startrow"]}:'\
        f'{number_to_letter(number_columns)}{access_last_row(dataframe)}'
    border_format_1 = worksheet_properties['conditional_formats']['border_format_1']
    border_format_2 = worksheet_properties['conditional_formats']['border_format_2']
    border_format_1['format'] = font_format
    border_format_2['format'] = font_format
    worksheet.conditional_format(worksheet_range, border_format_1)
    worksheet.conditional_format(worksheet_range, border_format_2)


def set_dataframe_format(worksheet, font_format):
    for column in worksheet_properties['column_formats']:
        worksheet.set_column(column.column_range, column.width, font_format)


def set_footer_title(worksheet, last_column, last_row, font_format):
    footer_title_row = last_row + 1
    footer_title_range = f'A{footer_title_row}:{last_column}{footer_title_row}'
    worksheet.set_row(last_row, worksheet_properties['footer_title_height'])
    worksheet.merge_range(footer_title_range, worksheet_properties['footer_title_content'], font_format)


def set_footer(worksheet, last_column, last_row, font_format):
    footer_row = last_row + 2
    footer_range = f'A{footer_row}:{last_column}{footer_row}'
    worksheet.set_row((footer_row - 1), worksheet_properties['footer_height'])
    worksheet.merge_range(footer_range, worksheet_properties['footer_content'], font_format)


def add_footer_row(dataframe, worksheet, font_formats):
    last_column = number_to_letter(count_columns(dataframe))
    last_row = access_last_row(dataframe)
    set_footer_title(worksheet, last_column, last_row, font_formats['footer_title'])
    set_footer(worksheet, last_column, last_row, font_formats['footer'])


def add_content(dataframe, worksheet, font_formats, client=None, legal=None):
    add_title_row(dataframe, worksheet, font_formats, client, legal)
    add_dataframe_headers(dataframe, worksheet, font_formats['datatype'])
    set_worksheet_border(dataframe, worksheet, font_formats['border'])
    add_footer_row(dataframe, worksheet, font_formats)


def format_xlsx_document(writer, dataframe, client=None, legal=None):
    font_formats, workbook = format_workbook(writer)
    worksheet = format_worksheet(writer)
    set_dataframe_format(worksheet, font_formats['body'])
    add_content(dataframe, worksheet, font_formats, client, legal)
    return workbook


def close_workbook(workbook):
    workbook.close()


def save_xlsx_document(writer):
    writer.save()


def finalize_xlsx_document(writer, dataframe, client=None, legal=None):
    workbook = format_xlsx_document(writer, dataframe, client, legal)
    # save_xlsx_document(writer)
    close_workbook(workbook)


def export_document(target_directory, file_name, dictionary, client=None, legal=None):
    prepare_output_environment(target_directory)
    dataframe = transform_dictionary(dictionary)
    writer = create_xlsx_document(file_name, dataframe)
    finalize_xlsx_document(writer, dataframe, client, legal)
