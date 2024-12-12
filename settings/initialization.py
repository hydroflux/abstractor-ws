import os

from classes.Abstract import Abstract
from classes.counties import county_dictionary

from engines.armadillo.transform import transform as transform_armadillo
from engines.buffalo.transform import transform as transform_buffalo
from engines.dolphin.transform import transform as transform_dolphin
from engines.eagle.transform import transform as transform_eagle
from engines.jaguar.transform import transform as transform_jaguar
from engines.komodo.transform import transform as transform_komodo
from engines.leopard.transform import transform as transform_leopard
from engines.mountain_lion.transform import \
    transform as transform_mountain_lion
from engines.manta_ray.transform import transform as transform_manta_ray
from engines.octopus.transform import transform as transform_octopus
from engines.platypus.transform import transform as transform_platypus
from engines.rabbit.transform import transform as transform_rabbit
from engines.swordfish.transform import transform as transform_swordfish

from project_management.generate_document_list import generate_document_list
from project_management.user_prompts import get_program_type

from settings.county_variables.general import (abstraction_type, download,
                                               headless)
from settings.objects.abstract_dataframe import \
    abstract_dictionary as dataframe
from settings.settings import (county_name, end_date, file_name, quarter,
                               range, search_name, section, sheet_name,
                               start_date, target_directory, township)

from dateutil import parser
from datetime import datetime

# from classes.Engine import Engine


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


def convert_to_mmddyyyy(date_str: str) -> str:
    """
    Convert any date string format to "MM/DD/YYYY".

    Args:
        date_str (str): The date string to convert.

    Returns:
        str: The date string in "MM/DD/YYYY" format.
    """
    try:
        # Parse the date string to a datetime object
        date_obj = parser.parse(date_str)
        # Format the datetime object to "MM/DD/YYYY"
        return date_obj.strftime("%m/%d/%Y")
    except (ValueError, parser.ParserError) as e:
        print(f"Error parsing date string '{date_str}': {e}")
        return None


def convert_to_long_form(date_str: str) -> str:
    """
    Convert a date string from "MM/DD/YYYY" format to long form (e.g., "November 01, 2024").

    Args:
        date_str (str): The date string in "MM/DD/YYYY" format to convert.

    Returns:
        str: The date string in long form.
    """
    try:
        # Parse the date string to a datetime object
        date_obj = datetime.strptime(date_str, "%m/%d/%Y")
        # Format the datetime object to long form
        return date_obj.strftime("%B %d, %Y")
    except ValueError as e:
        print(f"Error parsing date string '{date_str}': {e}")
        return None


# Some of these assignments could be handled on the "Abstract" class rather than here since they're static attributes
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
        start_date=convert_to_mmddyyyy(start_date),
        end_date=convert_to_mmddyyyy(end_date),
        legal=[
                section,
                township,
                range,
                quarter
            ]
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
    elif abstract.program == 'legal':
        section, township, range, quarter = abstract.legal
        abstract.file_name = f'{abstract.county.prefix}-T{township}N-R{range}W-{section}-{quarter}-LEGAL-SEARCH'


def handle_program_type(abstract):
    program_type_update(abstract)
    if abstract.program in ['name_search', 'legal']:
        return
    else:
        abstract.document_list = generate_document_list(target_directory, file_name, sheet_name)


def update_abstract_and_county_attributes(abstract):
    if abstract.county.engine == "armadillo":
        transform_armadillo(abstract)
    elif abstract.county.engine == "buffalo":
        transform_buffalo(abstract)
    elif abstract.county.engine == "dolphin":
        transform_dolphin(abstract)
    elif abstract.county.engine == "eagle":
        transform_eagle(abstract)
    elif abstract.county.engine == "jaguar":
        transform_jaguar(abstract)
    elif abstract.county.engine == "komodo":
        transform_komodo(abstract)
    elif abstract.county.engine == "leopard":
        transform_leopard(abstract)
    elif abstract.county.engine == "mountain_lion":
        transform_mountain_lion(abstract)
    elif abstract.county.engine == "manta_ray":
        transform_manta_ray(abstract)
    elif abstract.county.engine == "octopus":
        transform_octopus(abstract)
    elif abstract.county.engine == "platypus":
        transform_platypus(abstract)
    elif abstract.county.engine == "rabbit":
        transform_rabbit(abstract)
    elif abstract.county.engine == "swordfish":
        transform_swordfish(abstract)


def create_folder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory ' + directory)


def initialize_abstraction():
    abstract = create_abstract_object()
    handle_program_type(abstract)
    update_abstract_and_county_attributes(abstract)
    return abstract
