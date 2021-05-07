import sys

sys.path.append(".")

print("environment", __name__)
if __name__ == '__main__':
    from eagle.execute import execute_program as execute_eagle
    from eagle.execute import execute_review as review_eagle
    from leopard.execute import execute_program as execute_leopard
    from leopard.execute import execute_review as review_leopard
    from settings.general_functions import (get_county_data,
                                            start_program_timer,
                                            stop_program_timer)
    from settings.import_list import generate_document_list
    from settings.settings import (county_name, download, file_name, headless,
                                   sheet_name, target_directory, web_directory)
    from settings.user_prompts import get_program_type
else:
    from .eagle.execute import execute_program as execute_eagle
    from .eagle.execute import execute_review as review_eagle
    from .settings.settings import (county_name, download, file_name, headless,
                                    programs, sheet_name, target_directory,
                                    web_directory)
    from .tiger.execute import execute_web_program    


def execute_program_type(county, program_type, document_list):
    if county.program == 'eagle':
        if program_type == "execute":
            execute_eagle(county, target_directory, document_list, file_name, download)
        elif program_type == "review":
            review_eagle(county, target_directory, document_list, download)
    elif county.program == 'leopard':
        if program_type == "execute":
            execute_leopard(headless, target_directory, county, file_name, sheet_name, download)
        elif program_type == "review":
            review_leopard(target_directory, file_name, sheet_name)
    else:
        print(f'{county} does not match available execution options, please review.')


def execute_abstractor():
    county = get_county_data(county_name)
    document_list = generate_document_list(target_directory, file_name, sheet_name)
    program_type = get_program_type()
    start_time = start_program_timer(county)
    execute_program_type(county, program_type, document_list)
    stop_program_timer(start_time)
    quit()


execute_abstractor()
