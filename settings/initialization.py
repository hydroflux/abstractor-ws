from settings.classes.Abstract import Abstract
from settings.classes.counties import county_dictionary
from settings.general_functions import start_program_timer
from settings.import_list import generate_document_list
from settings.settings import (county_name, file_name, headless, sheet_name, download,
                               target_directory)
from settings.user_prompts import (add_download_types, currently_unavailable,
                                   get_demo_information, get_program_type,
                                   prepare_name_search)


def access_county_instance(county_name):
    county_instance = county_dictionary.get(county_name.lower())
    print(county_instance)
    return county_instance


def create_abstract_object():
    return Abstract(
        county=access_county_instance(county_name),
        target_directory=target_directory,
        program_type=get_program_type(),
        download=download
    )


def initialize_abstraction():
    abstract = create_abstract_object()
    abstract.document_list = generate_document_list(target_directory, file_name, sheet_name)
    abstract.timer = start_program_timer(abstract.county, abstract.document_list)
    return abstract
