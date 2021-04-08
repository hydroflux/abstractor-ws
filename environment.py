print("environment", __name__)
if __name__ == '__main__':
    from eagle.execute import execute_program as execute_eagle
    from eagle.execute import execute_review as review_eagle
    from settings.settings import (headless, county, download, file_name, programs,
                                   sheet_name, target_directory, web_directory)
    from settings.user_prompts import get_program_type

    # from tiger.execute import execute_web_program
else:
    from .eagle.execute import execute_program
    from .settings.settings import (download, file_name, sheet_name,
                                    target_directory, web_directory)
    from .tiger.execute import execute_web_program


program_type = get_program_type()
if county == programs["eagle"]:
    if program_type == "execute":
        execute_eagle(county, target_directory, file_name, sheet_name, download)
    elif program_type == "review":
        review_eagle(target_directory, file_name, sheet_name)
