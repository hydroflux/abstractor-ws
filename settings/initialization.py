import os
from typing import Literal, Optional, Union

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
from datetime import datetime, date

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


def convert_to_yyyymmdd(date_input) -> str:
    """
    Convert any date string format or date object to "YYYY,MM,DD".

    Args:
        date_input (Union[str, date]): The date string or date object to convert.

    Returns:
        str: The date string in "YYYY,MM,DD" format.
    """
    try:
        if isinstance(date_input, str):
            # Parse the date string to a datetime object
            date_obj = parser.parse(date_input)
        elif isinstance(date_input, date):
            # Use the date object directly
            date_obj = date_input
        else:
            raise ValueError("Invalid date input type. Must be a string or date object.")
        
        # Format the datetime object to "YYYY,MM,DD"
        return date_obj.strftime("%Y,%m,%d")
    except (ValueError, parser.ParserError) as e:
        print(f"Error parsing date input '{date_input}': {e}")
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
        start_date=start_date,
        end_date=end_date,
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


# Create folder is also a method that could be handled on the "Abstract" class; please review
def create_folder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory ' + directory)


def is_valid_date(date_str: str) -> bool:
    """
    Check if the given date string is valid.

    Args:
        date_str (str): The date string to check.

    Returns:
        bool: True if the date string is valid, False otherwise.
    """
    try:
        datetime.strptime(date_str, "%m/%d/%Y")
        return True
    except ValueError:
        return False


def convert_to_mmddyyyy(date_input: Union[str, date]) -> str:
    """
    Convert any date string format or date object to "MM/DD/YYYY".

    Args:
        date_input (Union[str, date]): The date string or date object to convert.

    Returns:
        str: The date string in "MM/DD/YYYY" format.
    """
    if isinstance(date_input, str):
        date_obj = datetime.strptime(date_input, "%m/%d/%Y")
    elif isinstance(date_input, date):
        date_obj = date_input
    else:
        raise ValueError("Invalid date input type. Must be a string or date object.")
    return date_obj.strftime("%m/%d/%Y")


def valid_initial_date(abstract: Abstract, date_attr: str) -> Optional[Literal[True]]:
    """
    Validate the initial date in the abstract.

    Args:
        abstract (Abstract): The abstract object to validate.
        date_attr (str): The date attribute to validate.

    Returns:
        Optional[Literal[True]]: True if the date is valid or None if invalid.
    """
    date_value = abstract[date_attr]
    if date_value is None:
        return True
    elif not is_valid_date(date_value):
        print(f"The {date_attr} is invalid, please check the date and try again.")
    else:
        abstract[date_attr] = convert_to_mmddyyyy(date_value)
        return True


def check_dates(abstract: dict) -> Optional[Literal[True]]:
    """
    Check the validity of start and end dates in the abstract.

    Args:
        abstract (dict): The abstract dictionary containing date attributes.

    Returns:
        Optional[Literal[True]]: True if the dates are valid or None if invalid.
    """
    today = convert_to_mmddyyyy(date.today())
    if valid_initial_date(abstract, "start_date") and valid_initial_date(abstract, "end_date"):
        start_date = abstract["start_date"]
        end_date = abstract["end_date"]
        if start_date is None and end_date is None:
            return True
        elif start_date and start_date > today:
            print("The start date is after today's date, please check the dates and try again.")
        elif end_date and end_date > today:
            print("The end date is after today's date, please check the dates and try again.")
        elif start_date and end_date and start_date > end_date:
            print("The start date is after the end date, please check the dates and try again.")
        else:
            return True


def initialize_abstraction():
    abstract = create_abstract_object()
    if check_dates(abstract):
        handle_program_type(abstract)
        update_abstract_and_county_attributes(abstract)
        return abstract
    else:
        quit()
