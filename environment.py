from .eagle.execute import execute_program
from settings.variables import (download, file_name, sheet_name,
                                target_directory, web_directory)
from tiger.execute import execute_web_program

county = 'ADAMS'
client = 'Client Test'
legal = 'Legal Test'
upload_file = 'Test'

# execute_program(target_directory, file_name, sheet_name, download)
execute_web_program(county, client, legal, upload_file)
