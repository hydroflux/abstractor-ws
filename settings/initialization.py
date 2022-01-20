import os
import shutil

from settings.classes.Abstract import Abstract
from settings.classes.counties import county_dictionary
from settings.general_functions import start_program_timer
from settings.import_list import generate_document_list
from settings.objects.abstract_dataframe import \
    abstract_dictionary as dataframe
from settings.settings import (county_name, download, file_name, headless,
                               sheet_name, target_directory)
from settings.user_prompts import get_program_type


def access_county_instance(county_name):
    county_instance = county_dictionary.get(county_name.lower())
    print(county_instance)
    return county_instance


def create_abstract_object():
    return Abstract(
        county=access_county_instance(county_name),
        target_directory=target_directory,
        file_name=file_name,
        program=get_program_type(),
        headless=headless,
        download=download,
        dataframe=dataframe
    )


def program_type_update(abstract):
    if abstract.program == "review":
        abstract.review = True
    elif abstract.program == "download":
        abstract.download_only = True


def create_folder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory ' + directory)


def create_document_directory(target_directory):
    document_directory = f'{target_directory}/Documents'
    create_folder(document_directory)
    os.chdir(document_directory)
    return document_directory


def initialize_abstraction():
    abstract = create_abstract_object()
    program_type_update(abstract)
    abstract.document_list = generate_document_list(target_directory, file_name, sheet_name)
    abstract.timer = start_program_timer(abstract.county, abstract.document_list)
    abstract.document_directory = create_document_directory(abstract.target_directory)
    return abstract


def move_abstraction_into_project_folder(target_directory, project_folder, abstraction):
    # shutil.move(f'{target_directory}/{file_name}-{abstraction_type.upper()}.xlsx', project_folder)
    shutil.move(f'{target_directory}/{abstraction}', project_folder)


def move_downloaded_documents(target_directory, project_folder):
    if download:
        shutil.move(f'{target_directory}/Documents', project_folder)


def bundle_project(abstract):
    os.chdir(abstract.target_directory)
    project_folder = abstract.create_project_folder()
    move_abstraction_into_project_folder(abstract.target_directory, project_folder, abstract.abstraction)
    move_downloaded_documents(abstract.target_directory, project_folder)
    # shutil.move(f'{target_directory}/{file_name}.xlsx', project_folder)
