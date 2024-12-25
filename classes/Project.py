from datetime import date
import os
import shutil
from pandas import DataFrame, ExcelWriter

from project_management.export_settings.content import number_to_letter
from project_management.export_settings.worksheet_properties import worksheet_properties
from project_management.export_settings.authorship import authorship, disclaimers
from project_management.export_settings.conditional_formatting import add_conditional_formatting
from project_management.export_settings.content import add_content, number_to_letter
from project_management.export_settings.hyperlinks import add_hyperlink_sheet

from settings.county_variables.general import abstraction_type
from settings.initialization import convert_to_yyyymmdd
from settings.settings import (client, document_order, prospect,
                               quarter, section, township, range as legal_range)

class Breakpoint:
    def __init__(self, title, position):
        self.title = title
        self.position = position

class ColumnFormat:
    def __init__(self, column_name, width):
        self.column_name = column_name
        self.width = width

class Project:
    # Static Class Variables
    authorship = authorship
    client_information = f'{client} - {prospect}'
    worksheet_properties = worksheet_properties
    text_formats = worksheet_properties["text_formats"]
    conditional_formats = worksheet_properties["conditional_formats"]

    def __init__(self, abstract):
        self.abstract = abstract
        self.disclaimer = self.set_disclaimer_type()
        self.type = abstract.type
        self.county = abstract.county
        self.target_directory = abstract.target_directory
        self.dataframe = DataFrame(abstract.dataframe)
        self.output_file = self.create_output_file()
        self.sheet_name = abstract.type.upper()
        
        # Create target directory
        self.create_target_directory()

        # Convert breakpoints and column formats to objects
        self.worksheet_properties['breakpoints'] = [Breakpoint(**bp) for bp in self.worksheet_properties['breakpoints']]
        self.worksheet_properties['column_formats'] = [ColumnFormat(**cf) for cf in self.worksheet_properties['column_formats']]

        # Drop empty columns from the dataframe
        self.drop_empty_columns()

        self.writer = self.create_excel_writer()
        self.create_abstraction_object()

        self.workbook = self.writer.book
        self.worksheet = self.writer.sheets[self.sheet_name]
        self.number_columns = len(self.dataframe.columns)
        self.last_column = None
        self.last_row = None
        self.footer_row = None
        self.worksheet_range = None
        self.client = None
        self.legal = None
        self.project_folder = None

        # Generate text formats after workbook is set
        self.text_formats = self.generate_text_formats()

        # Set Header Content
        self.worksheet_properties['header_content'] = {
            'type': f'{abstraction_type}\n',
            'user': f'{client} - {prospect}\n',
            'scope': f'Township {township} North - Range {legal_range} West, Section {section}: {quarter}\n',
            'order': document_order,
            'start_date': abstract.start_date,
            'end_date': abstract.end_date,
            'county': ''
        }

        # Set project attributes
        self.set_project_attributes()

        # Format the Excel document
        self.format_xlsx_document()
    
    
    def set_disclaimer_type(self):
        if self.abstract.program == "name_search":
            return disclaimers["name_search"]
        elif self.abstract.program == "legal":
            return disclaimers["legal"]
        else:
            return disclaimers["base"]


    def create_output_file(self):
        abstract = self.abstract
        if abstract.program == "name_search":
            search_name = abstract.search_name
            if search_name is None:
                search_name = 'All Documents'
            else:
                search_name = search_name.title()
            start_date = abstract.start_date
            end_date = abstract.end_date
            if start_date is None and end_date is None:
                file = f'{search_name} (Earliest - Present)'
            elif start_date is None:
                file = f'{search_name} (Earliest - {convert_to_yyyymmdd(end_date)})'
            elif end_date is None:
                file = f'{search_name} ({convert_to_yyyymmdd(start_date)} - Present)'
            else:
                file = f'{search_name} ({convert_to_yyyymmdd(start_date)} - {convert_to_yyyymmdd(end_date)})'
            output_file = f'{abstract.county} - {file} ({convert_to_yyyymmdd(date.today())}).xlsx'
            return output_file
        else:
            abstraction_export = '-'.join(abstract.type.upper().split(' '))
            file = f'{abstract.file_name}-{abstraction_export}'
            return f'{file} ({convert_to_yyyymmdd(date.today())}).xlsx'

    def create_target_directory(self):
        try:
            if not os.path.exists(self.target_directory):
                os.makedirs(self.target_directory)
            os.chdir(self.target_directory)
        except OSError:
            print('Error: Creating directory ' + self.target_directory)

    def drop_empty_columns(self):
        """
        Drop columns from the dataframe if they contain only empty strings.

        Args:
            project (Project): The project instance containing the worksheet and dataframe.
        """
        columns_to_drop = []
        if self.dataframe["Volume"].str.strip().eq("").all():
            columns_to_drop.append("Volume")
            column_formats = self.worksheet_properties['column_formats']
            self.worksheet_properties['column_formats'] = [cf for cf in column_formats if cf.column_name != "Volume"]
        if self.dataframe["Document Link"].str.strip().eq("").all():
            columns_to_drop.append("Document Link")
            column_formats = self.worksheet_properties['column_formats']
            self.worksheet_properties['column_formats'] = [cf for cf in column_formats if cf.column_name != "Document Link"]

        # Drop columns from the dataframe
        self.dataframe.drop(columns=columns_to_drop, inplace=True)
        if len(columns_to_drop) == 2:
            self.worksheet_properties['datatype_content']['primary_datatype_columns'] = [*range(0, 8), *range(12, 16)]
            self.worksheet_properties['datatype_content']['secondary_datatype_columns'] = [*range(8, 12)]
            self.worksheet_properties['datatype_content']['custom_datatype_column'] = 8
            self.conditional_formats['no_record_format']['criteria'] = '=LEFT($P5, 19)="No document located"'
            self.conditional_formats['multi_documents_format']['criteria'] = '=LEFT($P5, 26)="Multiple documents located"'
            self.conditional_formats['no_image_format']['criteria'] = '=LEFT($P5, 27)="No document image available"'
        elif len(columns_to_drop) == 1:
            self.worksheet_properties['datatype_content']['primary_datatype_columns'] = [*range(0, 9), *range(13, 17)]
            self.worksheet_properties['datatype_content']['secondary_datatype_columns'] = [*range(9, 13)]
            self.worksheet_properties['datatype_content']['custom_datatype_column'] = 9
            self.conditional_formats['no_record_format']['criteria'] = '=LEFT($Q5, 19)="No document located"'
            self.conditional_formats['multi_documents_format']['criteria'] = '=LEFT($Q5, 26)="Multiple documents located"'
            self.conditional_formats['no_image_format']['criteria'] = '=LEFT($Q5, 27)="No document image available"'

    def create_excel_writer(self):
        return ExcelWriter(
            self.output_file,
            engine='xlsxwriter',
            datetime_format='mm/dd/yyyy',
            date_format='mm/dd/yyyy'
        )

    def update_dataframe(self):
        """
        Update the dataframe by renaming columns.
        """
        # Rename Legal Description
        self.dataframe = self.dataframe.rename({"Legal": "Legal Description"}, axis=1)
        # Rename Effective Date
        self.dataframe = self.dataframe.rename({"Effective Date": "Document Effective Date"}, axis=1)
        # View Dataframe Layout
        print(self.dataframe)

    def add_column(self, dataframe, current_position, column):
        dataframe.insert(current_position, column.title, '')

    def add_breakpoints(self):
        """
        Add breakpoints to the dataframe.
        """
        current_position = self.dataframe.columns.get_loc(self.worksheet_properties['breakpoint_start'])
        for column in self.worksheet_properties['breakpoints']:
            self.add_column(self.dataframe, current_position, column)
            current_position = current_position + column.position

    def create_abstraction_object(self):
        """
        Create the abstraction object by updating the dataframe and adding breakpoints.
        """
        self.update_dataframe()
        self.add_breakpoints()
        self.dataframe.to_excel(
            self.writer,
            sheet_name=self.sheet_name,
            startrow=self.worksheet_properties['startrow'],
            header=False,
            index=False
        )

    def create_project_folder(self):
        self.project_folder = f'{self.target_directory}/{self.output_file[:-5]}'
        try:
            if not os.path.exists(self.project_folder):
                os.makedirs(self.project_folder)
        except OSError:
            print('Error: Creating directory ' + self.project_folder)

    def generate_text_formats(self):
        return {
            'large': self.workbook.add_format(self.text_formats['large']),
            'small': self.workbook.add_format(self.text_formats['small']),
            'header': self.workbook.add_format(self.text_formats['header']),
            'datatype': self.workbook.add_format(self.text_formats['datatype']),
            'body': self.workbook.add_format(self.text_formats['body']),
            'border': self.workbook.add_format(self.text_formats['border']),
            'limitations': self.workbook.add_format(self.text_formats['limitations']),
            'disclaimer': self.workbook.add_format(self.text_formats['disclaimer']),
            'footer': self.workbook.add_format(self.text_formats['footer']),
            'hyperlink': self.workbook.add_format(self.text_formats['hyperlink']),
            'no_record': self.workbook.add_format(self.text_formats['no_record']),
            'multiple_documents': self.workbook.add_format(self.text_formats['multiple_documents']),
            'no_image': self.workbook.add_format(self.text_formats['no_image']),
            'out_of_county': self.workbook.add_format(self.text_formats['out_of_county'])
        }

    def set_project_attributes(self):
        """
        Set the project attributes.
        """
        # self.create_abstraction_object()
        self.last_column = number_to_letter(self.number_columns)
        self.last_row = len(self.dataframe.index) + self.worksheet_properties['startrow']
        self.footer_row = self.last_row + 1
        self.worksheet_range = (f'A{self.worksheet_properties["startrow"]}:'
                                f'{number_to_letter(self.number_columns)}{self.last_row}')

    def format_xlsx_document(self):
        """
        Format the Excel document.
        """
        self.workbook.set_properties(self.authorship)
        self.worksheet.set_landscape()
        self.worksheet.set_paper(self.worksheet_properties['paper_size'])
        self.worksheet.set_margins(left=0.25, right=0.25, top=0.75, bottom=0.75)
        self.worksheet.hide_gridlines(self.worksheet_properties['gridlines'])
        self.worksheet.freeze_panes(f'A{self.worksheet_properties["startrow"] + 1}')

    def export_document(self):
        """
        Export the document by adding content, conditional formatting, and hyperlinks.
        """
        add_content(self)
        add_conditional_formatting(self)
        add_hyperlink_sheet(self)
        self.workbook.close()

    def bundle_project(self):
        self.export_document()
        self.create_project_folder()
        # Move Output File into Project Folder
        shutil.move(f'{self.target_directory}/{self.output_file}', self.project_folder)
        # Move Downloaded Documents
        if self.abstract.download:
            shutil.move(f'{self.target_directory}/Documents', self.project_folder)
