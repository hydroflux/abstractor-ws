if __name__ == '__main__':
    from eagle.execute import execute_program
    from settings.settings import (download, file_name, sheet_name,
                                   target_directory, web_directory)
    from tiger.execute import execute_web_program
else:
    from .eagle.execute import execute_program
    from .settings.settings import (download, file_name, sheet_name,
                                    target_directory, web_directory)
    from .tiger.execute import execute_web_program


# execute_program(target_directory, file_name, sheet_name, download)
# execute_web_program(county, client, legal, upload_file)
execute_web_program("ADAMS", '', '', "CAPSTONE-TEST")
