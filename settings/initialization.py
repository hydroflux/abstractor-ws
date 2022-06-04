import os

from classes.Abstract import Abstract
# from classes.Engine import Engine
from classes.counties import county_dictionary
from engines.eagle.transform import transform as transform_eagle
from engines.jaguar.transform import transform as transform_jaguar
from engines.leopard.transform import transform as transform_leopard
from engines.mountain_lion.transform import transform as transform_mountain_lion
from engines.rabbit.transform import transform as transform_rabbit
from engines.octopus.transform import transform as transform_octopus

from project_management.generate_document_list import generate_document_list
from project_management.timers import start_program_timer
from project_management.user_prompts import get_program_type

from settings.objects.abstract_dataframe import \
    abstract_dictionary as dataframe
from settings.settings import (abstraction_type, county_name, download,
                               file_name, headless, sheet_name, search_name,
                               start_date, end_date, legal, target_directory)


# def update_engine_attributes(engine):
#     pass


# def create_engine_object():
#     engine = Engine(
#         name="",  # Need to pass name into the engine
#         county=access_county_instance(county_name),
#     )
#     update_engine_attributes(engine)
#     return engine


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
        dataframe=dataframe,
        search_name=search_name,
        start_date=start_date,
        end_date=end_date,
        legal=legal
    )


def program_type_update(abstract):
    if abstract.program == "review":
        abstract.review = True
        abstract.headless = False
        abstract.download = False
    elif abstract.program == "download":
        abstract.download_only = True
        abstract.download = True
    elif abstract.program == 'name_search':
        abstract.download = False
        abstract.download_only = False


def handle_program_type(abstract):
    program_type_update(abstract)
    if abstract.program in ['name_search', 'legal']:
        return
    else:
        abstract.document_list = generate_document_list(target_directory, file_name, sheet_name)


def update_abstract_and_county_attributes(abstract):
    if abstract.county.engine == "eagle":
        transform_eagle(abstract)
    elif abstract.county.engine == "jaguar":
        transform_jaguar(abstract)
    elif abstract.county.engine == "leopard":
        transform_leopard(abstract)
    elif abstract.county.engine == "mountain_lion":
        transform_mountain_lion(abstract)
    elif abstract.county.engine == "rabbit":
        transform_rabbit(abstract)
    elif abstract.county.engine == "octopus":
        transform_octopus(abstract)


def create_folder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory ' + directory)


def initialize_abstraction():
    abstract = create_abstract_object()
    handle_program_type(abstract)
    abstract.timer = start_program_timer(abstract.county, abstract.document_list)
    update_abstract_and_county_attributes(abstract)
    return abstract
