import os

from settings.file_management import (extrapolate_document_value,
                                      list_remaining_documents)
from settings.general_functions import report_execution_time, title_strip
from settings.import_list import generate_document_list
from settings.settings import root, search_name


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
    while user_input not in ["1", "2", "3"]:
        clear_terminal()
        print(f'You entered {user_input} Please enter 1, 2, 3, or 4:')
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
        program_type = "name_search"
    clear_terminal()
    return program_type


def currently_unavailable(county, program_type):
    print(f'There has not been a(n) "{program_type}" application path developed for '
          f'{county} to date, please review your inputs.')
    quit()


def request_yes_or_no(prompt):
    clear_terminal()
    user_input = input(f'{prompt} (Y/N) \n')
    while user_input.upper() not in ["Y", "N", "YES", "NO"]:
        clear_terminal()
        print(f'You entered {user_input} Please enter "Y" or "N"')
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
    return name


def continue_prompt(current_target_directory, current_file_name, current_sheet_name):
    return request_yes_or_no('Would you like to create another abstraction?')


def target_directory_prompt(current_target_directory):
    print(f'Current Directory: {current_target_directory}')
    if request_yes_or_no('Has the target directory changed?'):
        target_directory_input = input("Please enter the new target directory: \n")
        return f'{root}/{target_directory_input}'
    else:
        return current_target_directory


def available_file_names(target_directory):
    os.listdir(target_directory)


def file_name_prompt(current_file_name):
    print(f'Current File Name: {current_file_name}')
    if request_yes_or_no('Has the file name changed?'):
        file_name_input = input("Please enter the new file name: \n")
        return f'{file_name_input}'
    else:
        return current_file_name


def available_sheet_names():
    # Program should request sheet name from the user
    pass


def sheet_name_prompt(current_sheet_name):
    print(f'Current Sheet Name: {current_sheet_name}')
    if request_yes_or_no('Has the sheet name changed?'):
        sheet_name_input = input("Please enter the new sheet name: \n")
        return f'{sheet_name_input}'
    else:
        return current_sheet_name


def document_found(start_time, document_list, document, alt=None):
    if alt is None:
        print('Document located at '
              f'{extrapolate_document_value(document)} recorded, '
              f'{list_remaining_documents(document_list, document)} '
              f'({report_execution_time(start_time)})')
    elif alt == "review":
        input(f'Document located at {extrapolate_document_value(document)} found,'
              'please review & press enter to continue... '
              f'({list_remaining_documents(document_list, document)}) '
              f'({report_execution_time(start_time)})')
    elif alt == "download":
        print('Document located at '
              f'{extrapolate_document_value(document)} downloaded, '
              f'{list_remaining_documents(document_list, document)} '
              f'({report_execution_time(start_time)})')


def no_document_found(start_time, document_list, document, alt=None):
    if alt is None:
        print('No document found at '
              f'{extrapolate_document_value(document)}, '
              f'{list_remaining_documents(document_list, document)} '
              f'({report_execution_time(start_time)})')
    elif alt == "review":
        input(f'No document found at {extrapolate_document_value(document)}, '
              'please review & press enter to continue... '
              f'({list_remaining_documents(document_list, document)}) '
              f'({report_execution_time(start_time)})')


# Add an additional prompt for request for download
def request_more_information(current_target_directory, current_file_name, current_sheet_name):
    target_directory = target_directory_prompt(current_target_directory)
    available_file_names(target_directory)
    file_name, sheet_name = file_name_prompt(current_file_name)
    available_sheet_names()
    sheet_name = sheet_name_prompt(current_sheet_name)
    return generate_document_list(target_directory, file_name, sheet_name)
