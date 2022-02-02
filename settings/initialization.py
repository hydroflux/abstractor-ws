import os

from classes.Abstract import Abstract
from classes.Engine import Engine
from classes.counties import county_dictionary

from project_management.generate_document_list import generate_document_list
from project_management.timers import start_program_timer
from project_management.user_prompts import get_program_type

from settings.objects.abstract_dataframe import \
    abstract_dictionary as dataframe
from settings.settings import (abstraction_type, county_name, download,
                               file_name, headless, sheet_name,
                               target_directory)


def access_county_instance(county_name):
    county_instance = county_dictionary.get(county_name.lower())
    print(county_instance)
    return county_instance


def create_engine_object():
    return Engine(
        name="",
        county=access_county_instance(county_name)
    )


def create_abstract_object(engine):
    return Abstract(
        type=abstraction_type,
        engine=engine,
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


def initialize_abstraction():
    engine = create_engine_object()
    abstract = create_abstract_object(engine)
    program_type_update(abstract)
    abstract.document_list = generate_document_list(target_directory, file_name, sheet_name)
    abstract.timer = start_program_timer(abstract.county, abstract.document_list)
    return abstract
