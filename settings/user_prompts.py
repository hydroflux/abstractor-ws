import os

from classes.Document import Document
from classes.counties import county_list
from settings.general_functions import title_strip
from settings.settings import root, search_name, download


def clear_terminal():
    os.system("clear")


def get_program_type():
    clear_terminal()
    user_input = input('What would you like to do? \n'
                       '[1] Execute Program \n'
                       '[2] Review Output \n'
                       '[3] Download Documents \n'
                       '[4] Name Search \n'
                       )
    while user_input not in ["1", "2", "3", "4"]:
        clear_terminal()
        print(f'You entered "{user_input}" Please enter 1, 2, 3, or 4:')
        user_input = input('What would you like to do? \n'
                           '[1] Execute Program \n'
                           '[2] Review Output \n'
                           '[3] Download Documents \n'
                           '[4] Name Search \n'
                           )
    if user_input == "1":
        program_type = "execute"
    elif user_input == "2":
        program_type = "review"
    elif user_input == "3":
        program_type = "download"
    elif user_input == "4":
        program_type = "name search"
    clear_terminal()
    return program_type


def currently_unavailable(abstract):
    print(f'There has not been a(n) "{abstract.program}" application path developed for '
          f'{abstract.county} to date, please review your inputs and try again.')
    quit()


def request_yes_or_no(prompt):
    clear_terminal()
    user_input = input(f'{prompt} (Y/N) \n')
    while user_input.upper() not in ["Y", "N", "YES", "NO"]:
        clear_terminal()
        print(f'You entered "{user_input}" Please enter "Y" or "N"')
        user_input = input(f'{prompt} (Y/N) \n')
    if user_input.upper() in ["Y", "YES"]:
        return True
    else:
        return False


def request_new_name():
    return input("Please enter the name you would like to search: \n")


def prepare_name_search():
    name = title_strip(search_name)
    if name == '':
        name = request_new_name()
    while request_yes_or_no(f'The current name to be searched is "{name}", is this correct?') is False:
        clear_terminal()
        name = request_new_name()
    clear_terminal()
    return Document(type="name", value=name)


def continue_prompt(current_target_directory, current_file_name, current_sheet_name):
    return request_yes_or_no('Would you like to create another abstraction?')


def target_directory_prompt(current_target_directory):
    print(f'Current Directory: {current_target_directory}')
    if request_yes_or_no('Has the target directory changed?'):
        target_directory_input = input("Please enter the new target directory: \n")
        return f'{root}/{target_directory_input}'
    else:
        return current_target_directory


def state_prompt():
    clear_terminal()
    state_input = input('Please choose a state in which to create an abstraction: \n'
                        '[1] Colorado \n'
                        '[2] Louisiana \n'
                        '[3] Texas \n'
                        '[4] Wyoming \n'
                        )
    while state_input not in ["1", "2", "3", "4"]:
        clear_terminal()
        print(f'You entered "{state_input}" Please enter 1, 2, 3, or 4:')
        state_input = input('Please choose a state in which to create an abstraction?: \n'
                            '[1] Colorado \n'
                            '[2] Louisiana \n'
                            '[3] Texas \n'
                            '[4] Wyoming \n'
                            )
    if state_input == "1":
        return 'CO'
    elif state_input == "2":
        return 'LA'
    elif state_input == "3":
        return 'TX'
    elif state_input == "4":
        return 'WY'


def filter_counties(state):
    return list(filter((lambda county: county.endswith(state)), county_list))


def get_county_options(state):
    available_counties = filter_counties(state)
    return list(map((lambda option: f'[{available_counties.index(option) + 1}] {option}'), available_counties))


def list_county_options(county_options):
    for option in county_options:
        print(option)


def check_for_county_match(county_options, county_input):
    for index, option in enumerate(county_options):
        if county_input == str(index + 1):
            return option
    return False


def get_county_name(county_options, county_input):
    return ' '.join(county_options[int(county_input) - 1].split()[1:])


def get_county_information(county_options):
    print('Please choose a county in which to create an abstraction:')
    list_county_options(county_options)
    county_input = input()
    while not check_for_county_match(county_options, county_input):
        print(f'You entered "{county_input}", please choose an item from the list below:')
        list_county_options(county_options)
        county_input = input()
    return get_county_name(county_options, county_input)


def county_prompt(state):
    clear_terminal()
    county_options = get_county_options(state)
    return get_county_information(county_options)


def get_demo_information():
    state = state_prompt()
    county = county_prompt(state)
    clear_terminal()
    print(f'Preparing an abstraction for "{county}"...')
    return county.split()[0]


def available_file_names(target_directory):
    os.listdir(target_directory)


def file_name_prompt(current_file_name):
    print(f'Current File Name: "{current_file_name}"')
    if request_yes_or_no('Has the file name changed?'):
        file_name_input = input("Please enter the new file name: \n")
        return f'{file_name_input}'
    else:
        return current_file_name


def available_sheet_names():
    # Program should request sheet name from the user
    pass


def sheet_name_prompt(current_sheet_name):
    print(f'Current Sheet Name: "{current_sheet_name}"')
    if request_yes_or_no('Has the sheet name changed?'):
        sheet_name_input = input("Please enter the new sheet name: \n")
        return f'{sheet_name_input}'
    else:
        return current_sheet_name


def download_type_prompt(county):
    print(f'\nYou are currently accessing "{county}", and have a choice between free or paid downloads.')
    input_statement = ('Would you prefer paid or free downloads: \n'
                       '[1] Free \n'
                       '[2] Paid \n'
                       )
    download_type_input = input(input_statement).lower()
    while download_type_input not in ['1', 'f', 'free', '2', 'p', 'paid']:
        clear_terminal()
        print(f'You entered "{download_type_input}" Please choose from the following options')
        download_type_input = input(input_statement).lower()
    if download_type_input in ['1', 'f', 'free']:
        return 'free'
    elif download_type_input in ['2', 'p', 'paid']:
        return 'paid'


def update_document_download_types(download_type, document_list):
    for document in document_list:
        document.download_type = download_type


def add_download_types(county, document_list):
    if download:
        download_type = download_type_prompt(county)
        update_document_download_types(download_type, document_list)
        clear_terminal()


# Add an additional prompt for request for download
# def request_more_information(current_target_directory, current_file_name, current_sheet_name):
#     target_directory = target_directory_prompt(current_target_directory)
#     available_file_names(target_directory)
#     file_name, sheet_name = file_name_prompt(current_file_name)
#     available_sheet_names()
#     sheet_name = sheet_name_prompt(current_sheet_name)
#     return generate_document_list(target_directory, file_name, sheet_name)
