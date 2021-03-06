import os
import shutil

from project_management.export_settings.settings import (authorship,
                                                         disclaimer,
                                                         text_formats,
                                                         worksheet_properties)


class Project:

    authorship = authorship
    disclaimer = disclaimer
    text_formats = text_formats
    worksheet_properties = worksheet_properties

    def __init__(self, type, county, target_directory, dataframe,
                 output_file, sheet_name,
                 writer=None, font_formats=None, workbook=None, worksheet=None,
                 number_columns=None, last_column=None, last_row=None, footer_row=None,
                 worksheet_range=None,
                 client=None, legal=None,
                 project_folder=None):
        self.type = type
        self.county = county
        self.target_directory = target_directory
        self.dataframe = dataframe
        self.output_file = output_file
        self.sheet_name = sheet_name
        self.writer = writer
        self.font_formats = font_formats
        self.workbook = workbook
        self.worksheet = worksheet
        self.number_columns = number_columns
        self.last_column = last_column
        self.last_row = last_row
        self.footer_row = footer_row
        self.worksheet_range = worksheet_range
        self.client = client
        self.legal = legal
        self.project_folder = project_folder

    def create_project_folder(self):
        self.project_folder = f'{self.target_directory}/{self.output_file[:-5]}'
        try:
            if not os.path.exists(self.project_folder):
                os.makedirs(self.project_folder)
        except OSError:
            print('Error: Creating directory ' + self.project_folder)

    def bundle_project(self, abstract):
        os.chdir(self.target_directory)
        self.create_project_folder()
        # Move Output File into Project Folder
        shutil.move(f'{self.target_directory}/{self.output_file}', self.project_folder)
        # Move Downloaded Documents
        if abstract.download:
            shutil.move(f'{self.target_directory}/Documents', self.project_folder)
