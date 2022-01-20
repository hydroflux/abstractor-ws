import os
from pandas import DataFrame, ExcelWriter

from settings.classes.Project import Project

from settings.temp_hyperlink import write_temporary_hyperlinks
from settings.export_settings import (authorship, full_disclaimer,
                                      text_formats, worksheet_properties)


def update_dataframe(project):
    # Rename Legal Description
    project.dataframe.rename({"Legal": "Legal Description"}, axis=1)
    # Rename Effective Date
    project.dataframe.rename({"Effective Date": "Document Effective Date"}, axis=1)


def create_output_file(abstract):
    abstraction_export = '-'.join(abstract.type.upper().split(' '))
    return f'{abstract.file_name.upper()}-{abstraction_export}.xlsx'


def create_excel_writer(project):
    return ExcelWriter(
        project.file_name,
        engine='xlsxwriter',
        datetime_format='mm/dd/yyyy',
        date_format='mm/dd/yyyy')  # pylint: disable=abstract-class-instantiated


def initialize_project(abstract):
    project = Project(
        type=abstract.type,
        target_directory=abstract.target_directory,
        dataframe=DataFrame(abstract.dataframe),
        file_name=create_output_file(abstract),
        sheet_name=abstract.type.upper()
    )
    project.writer = create_excel_writer(project)
    update_dataframe(project)
    print(project.dataframe)
    os.chdir(project.target_directory)
    return project


def add_column(dataframe, current_position, column):
    dataframe.insert(current_position, column.title, '')


def add_breakpoints(dataframe):
    current_position = dataframe.columns.get_loc(worksheet_properties['breakpoint_start'])
    for column in worksheet_properties['breakpoints']:
        print('current_position', current_position)
        print('column', column)
        print(dataframe.columns)
        add_column(dataframe, current_position, column)
        current_position = current_position + column.position


def create_abstraction_object(project):
    # add_hyperlinks(target_directory, dataframe)
    add_breakpoints(project.dataframe)
    return project.dataframe.to_excel(
        project.writer,
        sheet_name=project.sheet_name,
        startrow=worksheet_properties['startrow'],
        header=False,
        index=False
    )


def access_workbook_object(project):
    return project.writer.book


def access_worksheet_object(project):
    return project.writer.sheets[(project.sheet_name)]


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
        'limitations': workbook.add_format(text_formats['limitations']),
        'disclaimer': workbook.add_format(text_formats['disclaimer']),
        'footer': workbook.add_format(text_formats['footer']),
        'no_record': workbook.add_format(text_formats['no_record']),
        'multiple_documents': workbook.add_format(text_formats['multiple_documents']),
        'no_image': workbook.add_format(text_formats['no_image']),
        'out_of_county': workbook.add_format(text_formats['out_of_county'])
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


def format_worksheet(abstract, writer):
    worksheet = access_worksheet_object(abstract, writer)
    set_page_format(worksheet)
    return worksheet


def count_columns(dataframe):
    return len(dataframe.columns)


def number_to_letter(number):
    return chr(ord('@') + (number))


def last_column(dataframe):
    return number_to_letter(count_columns(dataframe))


def set_title_format(dataframe, worksheet, font_format):
    worksheet.set_row(0, worksheet_properties['header_height'])
    worksheet.merge_range(f'A1:{last_column(dataframe)}1', '', font_format)


def create_range_message(dataframe, content):
    return f'From {content["start_date"]} to {content["end_date"]} \n ({content["order"]})'


def write_title_content(dataframe, county, worksheet, font_formats, client=None, legal=None):
    content = worksheet_properties['header_content']
    content['county'] = f'{county}\n'
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


def add_title_row(county, dataframe, worksheet, font_formats, client=None, legal=None):
    set_title_format(dataframe, worksheet, font_formats['header'])
    write_title_content(dataframe, county, worksheet, font_formats, client, legal)


def add_limitations(dataframe, worksheet, font_format):
    worksheet.set_row(1, worksheet_properties['limitations_height'])
    worksheet.merge_range(f'A2:{last_column(dataframe)}2', worksheet_properties['limitations_content'], font_format)


def add_disclaimer(county, dataframe, worksheet, font_format):
    worksheet.set_row(2, worksheet_properties['disclaimer_height'])
    worksheet.merge_range(f'A3:{last_column(dataframe)}3', full_disclaimer(county), font_format)


def merge_primary_datatype_ranges(dataframe, worksheet, font_format):
    primary_range = worksheet_properties['datatype_content']['primary_datatype_columns']
    for column in primary_range:
        column_name = dataframe.columns[column]
        column_position = number_to_letter((column + 1))
        worksheet.merge_range(
            f'{column_position}4:{column_position}5',
            column_name,
            font_format
        )


def merge_custom_column(dataframe, worksheet, font_format):
    column = worksheet_properties['datatype_content']['custom_datatype_column']
    column_position_start = number_to_letter((column + 1))
    column_position_end = number_to_letter((column + 4))
    worksheet.merge_range(
        f'{column_position_start}4:{column_position_end}4',
        worksheet_properties['custom_column_name'],
        font_format
    )


def merge_secondary_datatype_ranges(dataframe, worksheet, font_format):
    primary_range = worksheet_properties['datatype_content']['secondary_datatype_columns']
    for column in primary_range:
        column_name = dataframe.columns[column]
        column_position = number_to_letter((column + 1))
        worksheet.write(
            f'{column_position}5',
            column_name,
            font_format
        )


def add_dataframe_headers(dataframe, worksheet, font_format):
    merge_primary_datatype_ranges(dataframe, worksheet, font_format)
    merge_custom_column(dataframe, worksheet, font_format)
    merge_secondary_datatype_ranges(dataframe, worksheet, font_format)


def access_last_row(dataframe):
    return len(dataframe.index) + worksheet_properties['startrow']


def get_worksheet_range(dataframe):
    number_columns = count_columns(dataframe)
    return (f'A{worksheet_properties["startrow"]}:'
            f'{number_to_letter(number_columns)}{access_last_row(dataframe)}')


def set_worksheet_border(dataframe, worksheet, font_format):
    worksheet_range = get_worksheet_range(dataframe)
    border_format_1 = worksheet_properties['conditional_formats']['border_format_1']
    border_format_2 = worksheet_properties['conditional_formats']['border_format_2']
    border_format_1['format'] = font_format
    border_format_2['format'] = font_format
    worksheet.conditional_format(worksheet_range, border_format_1)
    worksheet.conditional_format(worksheet_range, border_format_2)


def set_dataframe_format(worksheet, font_format):
    for column in worksheet_properties['column_formats']:
        worksheet.set_column(column.column_range, column.width, font_format)


def footer_row(dataframe):
    return access_last_row(dataframe) + 1


def add_footer_row(dataframe, worksheet, font_format):
    footer_range = f'A{footer_row(dataframe)}:{last_column(dataframe)}{footer_row(dataframe)}'
    worksheet.set_row((footer_row(dataframe) - 1), worksheet_properties['footer_height'])
    worksheet.merge_range(footer_range, worksheet_properties['footer_content'], font_format)


def add_filter(dataframe, worksheet):
    worksheet.autofilter(f'A5:{last_column(dataframe)}{footer_row(dataframe)}')


def add_watermark(worksheet):
    # Insert the watermark image in the header.
    worksheet.set_header('&C&G', {'image_center': 'draft_watermark.png'})
    worksheet.set_column('A:A', 50)
    # worksheet.write('A1', 'Select Print Preview to see the watermark.')


def add_content(county, dataframe, worksheet, font_formats, client=None, legal=None):
    add_title_row(county, dataframe, worksheet, font_formats, client, legal)
    add_limitations(dataframe, worksheet, font_formats['limitations'])
    add_disclaimer(county, dataframe, worksheet, font_formats['disclaimer'])
    add_dataframe_headers(dataframe, worksheet, font_formats['datatype'])
    set_worksheet_border(dataframe, worksheet, font_formats['border'])
    add_footer_row(dataframe, worksheet, font_formats['footer'])
    add_filter(dataframe, worksheet)
    # add_watermark(worksheet)


def add_no_record_format(worksheet, worksheet_range, font_format):
    no_record_format = worksheet_properties['conditional_formats']['no_record_format']
    no_record_format['format'] = font_format
    worksheet.conditional_format(worksheet_range, no_record_format)


def add_multiple_document_format(worksheet, worksheet_range, font_format):
    multi_documents_format = worksheet_properties['conditional_formats']['multi_documents_format']
    multi_documents_format['format'] = font_format
    worksheet.conditional_format(worksheet_range, multi_documents_format)


def add_no_document_image_format(worksheet, worksheet_range, font_format):
    no_document_image_format = worksheet_properties['conditional_formats']['no_image_format']
    no_document_image_format['format'] = font_format
    worksheet.conditional_format(worksheet_range, no_document_image_format)


def add_out_of_county_format(worksheet, worksheet_range, font_format):
    out_of_county_format = worksheet_properties['conditional_formats']['out_of_county_format']
    out_of_county_format['format'] = font_format
    worksheet.conditional_format(worksheet_range, out_of_county_format)


def add_conditional_formatting(dataframe, worksheet, font_formats):
    worksheet_range = get_worksheet_range(dataframe)
    add_no_record_format(worksheet, worksheet_range, font_formats['no_record'])
    add_multiple_document_format(worksheet, worksheet_range, font_formats['multiple_documents'])
    add_no_document_image_format(worksheet, worksheet_range, font_formats['no_image'])
    add_out_of_county_format(worksheet, worksheet_range, font_formats['out_of_county'])


def format_xlsx_document(abstract, writer, client=None, legal=None):
    font_formats, workbook = format_workbook(writer)
    worksheet = format_worksheet(abstract, writer)
    set_dataframe_format(worksheet, font_formats['body'])
    add_content(abstract.county, abstract.dataframe, worksheet, font_formats, client, legal)
    add_conditional_formatting(abstract.dataframe, worksheet, font_formats)
    return workbook


def create_hyperlink_sheet(workbook):
    hyperlink_sheet = workbook.add_worksheet("Hyperlink")
    hyperlink_sheet.set_column('A:A', 20)
    return hyperlink_sheet


def add_hyperlink_sheet(abstract, workbook):
    if abstract.download:
        hyperlink_format = workbook.add_format(text_formats['hyperlink'])
        hyperlink_sheet = create_hyperlink_sheet(workbook)
        write_temporary_hyperlinks(abstract.document_directory, hyperlink_sheet, hyperlink_format)
        os.chdir(abstract.target_directory)  # Is this necessary?


# def export_hyperlinks(abstract):
#     os.chdir(abstract.target_directory)
#     output_file, writer = create_xlsx_document(abstract.target_directory, abstract.file_name, abstract.dataframe)
#     workbook = access_workbook_object(writer)
#     add_hyperlink_sheet(abstract, workbook)
#     workbook.close()
#     return output_file


def export_document(abstract, client=None, legal=None):
    project = initialize_project(abstract)
    create_abstraction_object(project)
    workbook = format_xlsx_document(abstract, writer, client, legal)
    add_hyperlink_sheet(abstract, workbook)
    workbook.close()
