import sys

sys.path.append(".")

if __name__ == '__main__':
    from crocodile.execute import execute_program as execute_crocodile
    from crocodile.execute import execute_review as review_crocodile
    from eagle.execute import execute_document_download as download_eagle
    from eagle.execute import execute_program as execute_eagle
    from eagle.execute import execute_review as review_eagle
    from leopard.execute import execute_document_download as download_leopard
    from leopard.execute import execute_program as execute_leopard
    from leopard.execute import execute_review as review_leopard
    # from tiger.execute import execute_program as execute_tiger
    # from tiger.execute import execute_review as review_tiger
    from settings.general_functions import (get_county_data,
                                            start_program_timer,
                                            stop_program_timer)
    from settings.import_list import generate_document_list
    from settings.settings import (county_name, file_name, headless,
                                   sheet_name, target_directory)
    from settings.user_prompts import (currently_unavailable, get_program_type,
                                       prepare_name_search)

print("environment", __name__)


def execute_program_type(county, program_type, document_list):
    if county.program == 'crocodile':
        if program_type == 'execute':
            execute_crocodile(county, target_directory, document_list, file_name)
        elif program_type == 'review':
            review_crocodile()
        elif program_type == 'name search':
            search_name = prepare_name_search()
            # do something
    elif county.program == 'eagle':
        if program_type == "execute":
            execute_eagle(county, target_directory, document_list, file_name)
        elif program_type == "review":
            review_eagle(county, target_directory, document_list)
        elif program_type == "download":
            download_eagle(county, target_directory, document_list)
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
    else:
        print(f'{county} does not match available execution options, please review.')


def execute_abstractor():
    county = get_county_data(county_name)
    document_list = generate_document_list(target_directory, file_name, sheet_name)
    program_type = get_program_type()
    start_time = start_program_timer(county, document_list)
    execute_program_type(county, program_type, document_list)
    stop_program_timer(start_time)
    quit()


execute_abstractor()
