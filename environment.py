import sys

sys.path.append(".")

if __name__ == '__main__':
    from armadillo.execute import execute_program as execute_armadillo
    from crocodile.execute import execute_name_search as name_search_crocodile
    from crocodile.execute import execute_program as execute_crocodile
    from crocodile.execute import execute_review as review_crocodile
    # from eagle.execute import execute_document_download as download_eagle
    from eagle.execute import execute_program as execute_eagle
    from leopard.execute import execute_document_download as download_leopard
    from leopard.execute import execute_program as execute_leopard
    from leopard.execute import execute_review as review_leopard
    # from tiger.execute import execute_program as execute_tiger
    # from tiger.execute import execute_review as review_tiger
    from rattlesnake.execute import execute_program as execute_rattlesnake
    from settings.file_management import display_document_list
    from settings.general_functions import (get_county_data,
                                            start_program_timer,
                                            stop_program_timer)
    from settings.import_list import generate_document_list
    from settings.settings import (county_name, file_name, headless,
                                   sheet_name, target_directory)
    from settings.user_prompts import (add_download_types,
                                       currently_unavailable,
                                       get_demo_information, get_program_type,
                                       prepare_name_search)

print("environment", __name__)


def execute_program_type(county, program_type, document_list=None, search_name=None):
    if county.program == 'armadillo':
        if program_type == 'execute':
            add_download_types(county, document_list)
            execute_armadillo(county, target_directory, document_list, file_name)
        elif program_type == 'review':
            execute_armadillo(county, target_directory, document_list, file_name, True)
        else:
            currently_unavailable(county, program_type)
    elif county.program == 'crocodile':
        if program_type == 'execute':
            execute_crocodile(county, target_directory, document_list, file_name)
        elif program_type == 'review':
            review_crocodile()
        elif program_type == 'name search':
            name_search_crocodile(county, target_directory, search_name)
        else:
            currently_unavailable(county, program_type)
    elif county.program == 'eagle':
        if program_type == "execute":
            execute_eagle(county, target_directory, document_list, file_name)
        elif program_type == "review":
            execute_eagle(county, target_directory, document_list, file_name, True)
        # elif program_type == "download":
        #     download_eagle(county, target_directory, document_list)
        else:
            currently_unavailable(county, program_type)
    elif county.program == 'leopard':
        if program_type == "execute":
            execute_leopard(headless, county, target_directory, document_list, file_name, sheet_name)
        elif program_type == "review":
            review_leopard(county, target_directory, document_list)
        elif program_type == "download":
            download_leopard(county, target_directory, document_list)
        else:
            currently_unavailable(county, program_type)
    # elif county.program == 'tiger':
    #     if program_type == 'execute':
    #         execute_tiger()
    #     elif program_type == 'review':
    #         review_tiger()
    elif county.program == 'rattlesnake':
        if program_type == 'execute':
            add_download_types(county, document_list)
            execute_rattlesnake(county, target_directory, document_list, file_name)
        elif program_type == 'review':
            execute_rattlesnake(county, target_directory, document_list, file_name, True)
        else:
            currently_unavailable(county, program_type)
    else:
        print(f'"{county}" does not match available execution options, please review.')


# Break these out into simpler functions
def execute_abstractor():
    county = get_county_data(county_name)
    print(county)
    program_type = get_program_type()
    document_list = generate_document_list(target_directory, file_name, sheet_name)
    display_document_list(document_list)
    start_time = start_program_timer(county, document_list)
    execute_program_type(county, program_type, document_list)
    stop_program_timer(start_time)
    quit()


def execute_demo():
    county = get_county_data(get_demo_information())
    program_type = get_program_type()
    if program_type == "name search":
        search_name = prepare_name_search()
        start_time = start_program_timer(county)
        execute_program_type(county, program_type, document_list=None, search_name=search_name)
    else:
        document_list = generate_document_list(target_directory, file_name, sheet_name)
        start_time = start_program_timer(county)
        execute_program_type(county, program_type, document_list)
    stop_program_timer(start_time)
    quit()


execute_abstractor()
# execute_demo()
