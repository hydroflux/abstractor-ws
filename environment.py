from .execute import execute_program, execute_web_program
from .variables import download, file_name, sheet_name, target_directory, web_directory

execute_program(target_directory, file_name, sheet_name, download)
execute_web_program(client, legal, upload_file)