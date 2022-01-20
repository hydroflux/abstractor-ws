import os
from pandas import DataFrame, ExcelWriter

from settings.classes.Project import Project
from settings.export.conditional_formatting import add_conditional_formatting

from settings.temp_hyperlink import write_temporary_hyperlinks
from settings.export.settings import full_disclaimer


def update_dataframe(project):
    # Rename Legal Description
    project.dataframe = project.dataframe.rename({"Legal": "Legal Description"}, axis=1)
    # Rename Effective Date
    project.dataframe = project.dataframe.rename({"Effective Date": "Document Effective Date"}, axis=1)
    # View Dataframe Layout
    print(project.dataframe)


def create_output_file(abstract):
    abstraction_export = '-'.join(abstract.type.upper().split(' '))
    return f'{abstract.file_name.upper()}-{abstraction_export}.xlsx'


def create_excel_writer(project):
    return ExcelWriter(
        project.output_file,
        engine='xlsxwriter',
        datetime_format='mm/dd/yyyy',
        date_format='mm/dd/yyyy')  # pylint: disable=abstract-class-instantiated


def add_column(dataframe, current_position, column):
    dataframe.insert(current_position, column.title, '')


def add_breakpoints(dataframe):
    current_position = dataframe.columns.get_loc(Project.worksheet_properties['breakpoint_start'])
    for column in Project.worksheet_properties['breakpoints']:
        add_column(dataframe, current_position, column)
        current_position = current_position + column.position


def create_abstraction_object(project):
    update_dataframe(project)
    add_breakpoints(project.dataframe)
    project.dataframe.to_excel(
        project.writer,
        sheet_name=project.sheet_name,
        startrow=Project.worksheet_properties['startrow'],
        header=False,
        index=False
    )


def set_font_formats(project):
    return {
        'large': project.workbook.add_format(Project.text_formats['large']),
        'small': project.workbook.add_format(Project.text_formats['small']),
        'header': project.workbook.add_format(Project.text_formats['header']),
        'datatype': project.workbook.add_format(Project.text_formats['datatype']),
        'body': project.workbook.add_format(Project.text_formats['body']),
        'border': project.workbook.add_format(Project.text_formats['border']),
        'limitations': project.workbook.add_format(Project.text_formats['limitations']),
        'disclaimer': project.workbook.add_format(Project.text_formats['disclaimer']),
        'footer': project.workbook.add_format(Project.text_formats['footer']),
        'no_record': project.workbook.add_format(Project.text_formats['no_record']),
        'multiple_documents': project.workbook.add_format(Project.text_formats['multiple_documents']),
        'no_image': project.workbook.add_format(Project.text_formats['no_image']),
        'out_of_county': project.workbook.add_format(Project.text_formats['out_of_county'])
    }


def number_to_letter(number):
    return chr(ord('@') + (number))


def set_project_attributes(project):
    project.writer = create_excel_writer(project)
    create_abstraction_object(project)
    project.workbook = project.writer.book
    project.worksheet = project.writer.sheets[(project.sheet_name)]
    project.font_formats = set_font_formats(project)
    project.number_columns = len(project.dataframe.columns)
    project.last_column = number_to_letter(project.number_columns)
    project.last_row = len(project.dataframe.index) + project.worksheet_properties['startrow']
    project.footer_row = project.last_row + 1
    project.worksheet_range = (f'A{Project.worksheet_properties["startrow"]}:'
                               f'{number_to_letter(project.number_columns)}{project.last_row}')


def format_xlsx_document(project):
    # Format Workbook
    project.workbook.set_properties(Project.authorship)
    # Format Worksheet
    project.worksheet.set_landscape()
    project.worksheet.set_paper(Project.worksheet_properties['paper_size'])
    project.worksheet.set_margins(left=0.25, right=0.25, top=0.75, bottom=0.75)
    project.worksheet.hide_gridlines(Project.worksheet_properties['gridlines'])
    project.worksheet.freeze_panes(f'A{Project.worksheet_properties["startrow"] + 1}')


def initialize_project(abstract):
    os.chdir(abstract.target_directory)
    project = Project(
        type=abstract.type,
        county=abstract.county,
        target_directory=abstract.target_directory,
        dataframe=DataFrame(abstract.dataframe),
        output_file=create_output_file(abstract),
        sheet_name=abstract.type.upper()
    )
    set_project_attributes(project)
    format_xlsx_document(project)
    return project


def set_title_format(project, font_format):
    project.worksheet.set_row(0, Project.worksheet_properties['header_height'])
    project.worksheet.merge_range(f'A1:{project.last_column}1', '', font_format)


def create_range_message(dataframe, content):
    return f'From {content["start_date"]} to {content["end_date"]} \n ({content["order"]})'


def write_title_content(project):
    content = Project.worksheet_properties['header_content']
    content['county'] = f'{project.county}\n'
    range_message = create_range_message(project.dataframe, content)
    if project.client is not None and project.legal is not None:
        content['user'] = f'{project.client}\n'
        content['scope'] = f'{project.legal}\n'
    project.worksheet.write_rich_string(
        'A1',
        project.font_formats['large'], content['type'],
        project.font_formats['large'], content['user'],
        project.font_formats['small'], content['scope'],
        project.font_formats['small'], content['county'],
        project.font_formats['small'], range_message,
        project.font_formats['header']
    )


def add_title_row(project):
    set_title_format(project, project.font_formats['header'])
    write_title_content(project)


def add_limitations(project, font_format):
    project.worksheet.set_row(1, Project.worksheet_properties['limitations_height'])
    project.worksheet.merge_range(f'A2:{project.last_column}2',
                                  Project.worksheet_properties['limitations_content'],
                                  font_format)


def add_disclaimer(project, font_format):
    project.worksheet.set_row(2, Project.worksheet_properties['disclaimer_height'])
    project.worksheet.merge_range(f'A3:{project.last_column}3', full_disclaimer(project.county), font_format)


def merge_primary_datatype_ranges(project, font_format):
    primary_range = Project.worksheet_properties['datatype_content']['primary_datatype_columns']
    for column in primary_range:
        column_name = project.dataframe.columns[column]
        column_position = number_to_letter((column + 1))
        project.worksheet.merge_range(
            f'{column_position}4:{column_position}5',
            column_name,
            font_format
        )


def merge_custom_column(project, font_format):
    column = Project.worksheet_properties['datatype_content']['custom_datatype_column']
    column_position_start = number_to_letter((column + 1))
    column_position_end = number_to_letter((column + 4))
    project.worksheet.merge_range(
        f'{column_position_start}4:{column_position_end}4',
        Project.worksheet_properties['custom_column_name'],
        font_format
    )


def merge_secondary_datatype_ranges(project, font_format):
    primary_range = Project.worksheet_properties['datatype_content']['secondary_datatype_columns']
    for column in primary_range:
        column_name = project.dataframe.columns[column]
        column_position = number_to_letter((column + 1))
        project.worksheet.write(
            f'{column_position}5',
            column_name,
            font_format
        )


def add_dataframe_headers(project, font_format):
    merge_primary_datatype_ranges(project, font_format)
    merge_custom_column(project, font_format)
    merge_secondary_datatype_ranges(project, font_format)


def set_worksheet_border(project, font_format):
    border_format_1 = Project.worksheet_properties['conditional_formats']['border_format_1']
    border_format_2 = Project.worksheet_properties['conditional_formats']['border_format_2']
    border_format_1['format'] = font_format
    border_format_2['format'] = font_format
    project.worksheet.conditional_format(project.worksheet_range, border_format_1)
    project.worksheet.conditional_format(project.worksheet_range, border_format_2)


def set_dataframe_format(project):
    body_format = project.font_formats['body']
    for column in Project.worksheet_properties['column_formats']:
        project.worksheet.set_column(column.column_range, column.width, body_format)


def add_footer_row(project, font_format):
    footer_range = f'A{project.footer_row}:{project.last_column}{project.footer_row}'
    project.worksheet.set_row((project.last_row), Project.worksheet_properties['footer_height'])
    project.worksheet.merge_range(footer_range, Project.worksheet_properties['footer_content'], font_format)


def add_filter(project):
    project.worksheet.autofilter(f'A5:{project.last_column}{project.footer_row}')


# def add_watermark(project):
#     # Insert the watermark image in the header.
#     project.worksheet.set_header('&C&G', {'image_center': 'draft_watermark.png'})
#     project.worksheet.set_column('A:A', 50)
#     # worksheet.write('A1', 'Select Print Preview to see the watermark.')


def add_content(project):
    add_title_row(project)
    add_limitations(project, project.font_formats['limitations'])
    add_disclaimer(project, project.font_formats['disclaimer'])
    add_dataframe_headers(project, project.font_formats['datatype'])
    set_worksheet_border(project, project.font_formats['border'])
    set_dataframe_format(project)
    add_footer_row(project, project.font_formats['footer'])
    add_filter(project)
    # add_watermark(project)


def create_hyperlink_sheet(project):
    hyperlink_sheet = project.workbook.add_worksheet("Hyperlink")
    hyperlink_sheet.set_column('A:A', 20)
    return hyperlink_sheet


def add_hyperlink_sheet(abstract, project):
    if abstract.download:
        hyperlink_format = project.workbook.add_format(Project.text_formats['hyperlink'])
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


def export_document(abstract):
    project = initialize_project(abstract)
    add_content(project)
    add_conditional_formatting(project)
    add_hyperlink_sheet(abstract, project)
    project.workbook.close()
    return project
