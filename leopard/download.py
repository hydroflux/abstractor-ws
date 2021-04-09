from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from settings.download_management import update_download
from settings.file_management import create_document_directory
from settings.settings import timeout

from tiger.tiger_variables import (download_button_id, stock_download,
                                   view_group_id, view_panel_id)

# Use the following print statement to identify the best way to manage imports for Django vs the script folder
print("download", __name__)

