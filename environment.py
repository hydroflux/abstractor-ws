print("environment", __name__)
if __name__ == '__main__':
    from eagle.execute import execute_program, execute_review
    from settings.settings import (county, download, file_name, sheet_name,
                                   target_directory, web_directory)
    from settings.user_prompts import get_program_type
    # from tiger.execute import execute_web_program
else:
    from .eagle.execute import execute_program
    from .settings.settings import (download, file_name, sheet_name,
                                    target_directory, web_directory)
    from .tiger.execute import execute_web_program


execute_review(target_directory, file_name, sheet_name)
