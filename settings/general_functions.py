from datetime import datetime
from pprint import pprint
from random import randint
from time import sleep

from settings.classes.counties import county_dictionary
from settings.settings import abstraction_type


def naptime():
    # sleep(randint(3, 6))
    sleep(randint(2, 3))


def short_nap():
    sleep(randint(1, 2))


def long_nap():
    sleep(randint(30, 45))


def get_county_data(county_name):
    return county_dictionary.get(county_name)


def start_timer():
    return datetime.now()


def stop_timer(start_time):
    return datetime.now() - start_time


def report_execution_time(start_time):
    return str(stop_timer(start_time))


def start_program_timer(county):
    start_time = start_timer()
    print(f'{county} - {abstraction_type} started on: \n'
          f'{str(start_time.strftime("%B %d, %Y %H:%M:%S"))}')
    return start_time


def stop_program_timer(start_time):
    print(f'Total Run Time: {report_execution_time(start_time)}')
    

def scroll_into_view(browser, element):
    browser.execute_script("arguments[0].scrollIntoView();", element)


def javascript_script_execution(browser, script):
    browser.execute_script(script)


def get_element_text(element):
    return element.text.strip()


def title_strip(text):
    return text.title().strip()


def update_sentence_case_extras(text):
    return text.replace("'S ", "'s ").replace("1St ", "1st ").replace("2Nd ", "2nd ").replace("3Rd ", "3rd ").replace("4Th ", "4th ")

# def scroll_to_top(browser):
#     try:
#         body_element_present = EC.presence_of_element_located((By.TAG_NAME, "body"))
#         WebDriverWait(browser, timeout).until(body_element_present)
#         body_element = browser.find_element_by_tag_name("body")
#         browser.execute_script("arguments[0].scrollIntoView();", body_element)
#     except TimeoutException:
#         print("Timed out while trying to scroll to the top of the page.")


def scroll_to_top(browser):
    body_element = browser.find_element_by_tag_name("body")
    scroll_into_view(browser, body_element)


def get_element_attributes(browser, element):
    attributes = browser.execute_script('var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;', element)
    pprint(attributes)


def drop_last_entry(dataframe):
    dataframe["Grantor"].pop()
    dataframe["Grantee"].pop()
    dataframe["Book"].pop()
    dataframe["Page"].pop()
    dataframe["Reception Number"].pop()
    dataframe["Document Type"].pop()
    dataframe["Recording Date"].pop()
    dataframe["Legal"].pop()
    dataframe["Related Documents"].pop()
    dataframe["Comments"].pop()


def check_length(dataframe):
    grantors = len(dataframe["Grantor"])
    grantees = len(dataframe["Grantee"])
    books = len(dataframe["Book"])
    pages = len(dataframe["Page"])
    reception_numbers = len(dataframe["Reception Number"])
    document_types = len(dataframe["Document Type"])
    recording_dates = len(dataframe["Recording Date"])
    legals = len(dataframe["Legal"])
    related_documents = len(dataframe["Related Documents"])
    comments = len(dataframe["Comments"])
    if (grantors == grantees == books == pages == reception_numbers == document_types == recording_dates == legals == related_documents == comments):
        pass
    else:
        print("Grantors: ", grantors)
        print("Grantees: ", grantees)
        print("Books: ", books)
        print("Pages: ", pages)
        print("Reception Numbers: ", reception_numbers)
        print("Document Types: ", document_types)
        print("Recording Dates: ", recording_dates)
        print("Legals: ", legals)
        print("Related Documents: ", related_documents)
        print("Comments: ", comments)