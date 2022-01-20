import os
from pandas import DataFrame, ExcelWriter

from settings.classes.Project import Project
from settings.export.conditional_formatting import add_conditional_formatting
from settings.export.content import add_content, number_to_letter

from settings.temp_hyperlink import write_temporary_hyperlinks


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
