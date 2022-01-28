import os

from classes.Abstract import Abstract
from classes.counties import county_dictionary
from settings.general_functions import start_program_timer
from project_management.generate_document_list import generate_document_list
from settings.objects.abstract_dataframe import \
    abstract_dictionary as dataframe
from settings.settings import (county_name, download, file_name, headless, abstraction_type,
                               sheet_name, target_directory)
from project_management.user_prompts import get_program_type


def access_county_instance(county_name):
    county_instance = county_dictionary.get(county_name.lower())
    print(county_instance)
    return county_instance


def create_abstract_object():
    return Abstract(
        type=abstraction_type,
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
        abstract.headless = False
        abstract.download = False
    elif abstract.program == "download":
        abstract.download_only = True
        abstract.download = True


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


def prepare_for_download(abstract):
    abstract.document_directory = create_document_directory(abstract.target_directory)
    abstract.document_directory_files = len(os.listdir(abstract.document_directory))


def initialize_abstraction():
    abstract = create_abstract_object()
    program_type_update(abstract)
    abstract.document_list = generate_document_list(target_directory, file_name, sheet_name)
    abstract.timer = start_program_timer(abstract.county, abstract.document_list)
    return abstract
