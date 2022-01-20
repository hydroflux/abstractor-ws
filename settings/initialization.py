from settings.classes.Abstract import Abstract
from settings.classes.counties import county_dictionary
from settings.general_functions import start_program_timer
from settings.import_list import generate_document_list
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
        download=download
    )


def initialize_abstraction():
    abstract = create_abstract_object()
    abstract.document_list = generate_document_list(target_directory, file_name, sheet_name)
    abstract.timer = start_program_timer(abstract.county, abstract.document_list)
    return abstract
