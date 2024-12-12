# from pandas import DataFrame, ExcelWriter

# from classes.Project import Project

# from project_management.export_settings.conditional_formatting import add_conditional_formatting
# from project_management.export_settings.content import add_content, number_to_letter
# from project_management.export_settings.hyperlinks import add_hyperlink_sheet


# def drop_empty_columns(project):
#     """
#     Drop columns from the dataframe if they contain only empty strings.

#     Args:
#         project (Project): The project instance containing the worksheet and dataframe.
#     """
#     columns_to_drop = []
#     if project.dataframe["Volume"].str.strip().eq("").all():
#         columns_to_drop.append("Volume")
#         column_formats = project.worksheet_properties['column_formats']
#         project.worksheet_properties['column_formats'] = [cf for cf in column_formats if cf.column_name != "Volume"]
#     if project.dataframe["Document Link"].str.strip().eq("").all():
#         columns_to_drop.append("Document Link")
#         column_formats = project.worksheet_properties['column_formats']
#         project.worksheet_properties['column_formats'] = [cf for cf in column_formats if cf.column_name != "Document Link"]

#     # Drop columns from the dataframe
#     project.dataframe.drop(columns=columns_to_drop, inplace=True)
#     if len(columns_to_drop) == 2:
#         project.worksheet_properties['datatype_content']['primary_datatype_columns'] = [*range(0, 8), *range(12, 16)]
#         project.worksheet_properties['datatype_content']['secondary_datatype_columns'] = [*range(8, 12)]
#         project.worksheet_properties['datatype_content']['custom_datatype_column'] = 8
#         project.worksheet_properties['conditional_formats']['no_record_format']['criteria'] = '=LEFT($P5, 19)="No document located"'
#         project.worksheet_properties['conditional_formats']['multi_documents_format']['criteria'] = '=LEFT($P5, 26)="Multiple documents located"'
#         project.worksheet_properties['conditional_formats']['no_image_format']['criteria'] = '=LEFT($P5, 27)="No document image available"'
#     elif len(columns_to_drop) == 1:
#         project.worksheet_properties['datatype_content']['primary_datatype_columns'] = [*range(0, 9), *range(13, 17)]
#         project.worksheet_properties['datatype_content']['secondary_datatype_columns'] = [*range(9, 13)]
#         project.worksheet_properties['datatype_content']['custom_datatype_column'] = 9
#         project.worksheet_properties['conditional_formats']['no_record_format']['criteria'] = '=LEFT($Q5, 19)="No document located"'
#         project.worksheet_properties['conditional_formats']['multi_documents_format']['criteria'] = '=LEFT($Q5, 26)="Multiple documents located"'
#         project.worksheet_properties['conditional_formats']['no_image_format']['criteria'] = '=LEFT($Q5, 27)="No document image available"'


# def update_dataframe(project):
#     # Rename Legal Description
#     project.dataframe = project.dataframe.rename({"Legal": "Legal Description"}, axis=1)
#     # Rename Effective Date
#     project.dataframe = project.dataframe.rename({"Effective Date": "Document Effective Date"}, axis=1)
#     # View Dataframe Layout
#     print(project.dataframe)


# def create_output_file(abstract):
#     abstraction_export = '-'.join(abstract.type.upper().split(' '))
#     return f'{abstract.file_name.upper()}-{abstraction_export}.xlsx'


# def create_excel_writer(project):
#     return ExcelWriter(
#         project.output_file,
#         engine='xlsxwriter',
#         datetime_format='mm/dd/yyyy',
#         date_format='mm/dd/yyyy')  # pylint: disable=abstract-class-instantiated


# def add_column(dataframe, current_position, column):
#     dataframe.insert(current_position, column.title, '')


# def add_breakpoints(dataframe):
#     current_position = dataframe.columns.get_loc(Project.worksheet_properties['breakpoint_start'])
#     for column in Project.worksheet_properties['breakpoints']:
#         add_column(dataframe, current_position, column)
#         current_position = current_position + column.position


# def create_abstraction_object(project):
#     update_dataframe(project)
#     add_breakpoints(project.dataframe)
#     project.dataframe.to_excel(
#         project.writer,
#         sheet_name=project.sheet_name,
#         startrow=Project.worksheet_properties['startrow'],
#         header=False,
#         index=False
#     )


# def set_project_attributes(project):
#     project.writer = create_excel_writer(project)
#     create_abstraction_object(project)
#     project.workbook = project.writer.book
#     project.worksheet = project.writer.sheets[(project.sheet_name)]
#     project.text_formats = project.generate_text_formats()
#     project.number_columns = len(project.dataframe.columns)
#     project.last_column = number_to_letter(project.number_columns)
#     project.last_row = len(project.dataframe.index) + project.worksheet_properties['startrow']
#     project.footer_row = project.last_row + 1
#     project.worksheet_range = (f'A{Project.worksheet_properties["startrow"]}:'
#                                f'{number_to_letter(project.number_columns)}{project.last_row}')


# def format_xlsx_document(project):
#     # Format Workbook
#     project.workbook.set_properties(Project.authorship)
#     # Format Worksheet
#     project.worksheet.set_landscape()
#     project.worksheet.set_paper(Project.worksheet_properties['paper_size'])
#     project.worksheet.set_margins(left=0.25, right=0.25, top=0.75, bottom=0.75)
#     project.worksheet.hide_gridlines(Project.worksheet_properties['gridlines'])
#     project.worksheet.freeze_panes(f'A{Project.worksheet_properties["startrow"] + 1}')


# def initialize_project(abstract):
#     project = Project(
#         type=abstract.type,
#         county=abstract.county,
#         target_directory=abstract.target_directory,
#         abstract=abstract,
#         dataframe=DataFrame(abstract.dataframe),
#         output_file=create_output_file(abstract),
#         sheet_name=abstract.type.upper()
#     )
#     project.create_target_directory()
#     drop_empty_columns(project)  # Drop empty columns before adding content and formatting
#     set_project_attributes(project)
#     format_xlsx_document(project)
#     return project


# def export_document(abstract):
#     project = initialize_project(abstract)
#     add_content(project)
#     add_conditional_formatting(project)
#     add_hyperlink_sheet(abstract, project)
#     project.workbook.close()
#     return project
