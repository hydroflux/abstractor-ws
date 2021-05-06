print("environment", __name__)
if __name__ == '__main__':
    from eagle.execute import execute_program as execute_eagle
    from eagle.execute import execute_review as review_eagle
    from leopard.execute import execute_program as execute_leopard
    from leopard.execute import execute_review as review_leopard
    from settings.settings import (county, download, file_name, headless,
                                    programs, sheet_name, target_directory,
                                    web_directory)
    from settings.general_functions import start_program_timer, stop_program_timer
    from settings.user_prompts import get_program_type
else:
    from .eagle.execute import execute_program as execute_eagle
    from .eagle.execute import execute_review as review_eagle
    from .settings.settings import (county, download, file_name, headless,
                                    programs, sheet_name, target_directory,
                                    web_directory)
    from .tiger.execute import execute_web_program    


def execute_program_type(program_type):
    if county == programs["eagle"]:
        if program_type == "execute":
            execute_eagle(county, target_directory, file_name, sheet_name, download)
        elif program_type == "review":
            review_eagle(target_directory, file_name, sheet_name)
    elif county == programs["leopard"]:
        if program_type == "execute":
            execute_leopard(headless, target_directory, county, file_name, sheet_name, download)
        elif program_type == "review":
            review_leopard(target_directory, file_name, sheet_name)
    else:
        print(f'County {county} does not match available execution options, please review.')


def execute_abstractor():
    program_type = get_program_type()
    start_time = start_program_timer(county)
    execute_abstractor(program_type)
    stop_program_timer(start_time)
    browser.close()
    quit()


execute_abstractor()
