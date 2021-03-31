from .execute import execute_program
from tiger.execute import execute_web_program
from .variables import download, file_name, sheet_name, target_directory, web_directory


county = 'ADAMS'
client = 'Client Test'
legal = 'Legal Test'
upload_file = 'Test'

# execute_program(target_directory, file_name, sheet_name, download)
execute_web_program(county, client, legal, upload_file)
