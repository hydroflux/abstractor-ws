from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from leopard.leopard_variables import logout_button_id
from settings.settings import timeout

# Use the following print statement to identify the best way to manage imports for Django vs the script folder
print("logout", __name__)

def logout(browser):
    try:
        logout_button_present = EC.presence_of_element_located((By.ID, logout_button_id))
        WebDriverWait(browser, timeout).until(logout_button_present)
        logout_button = browser.find_element_by_id(logout_button_id)
        logout_link = logout_button.get_attribute("href")
        browser(logout_link)
    except TimeoutException:
        print("Browser timed out while trying to logout, please review.")
