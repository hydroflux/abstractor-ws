import os
from import_list import generate_document_list
from variables import root

def clear_terminal():
    os.system("clear")


def request_yes_or_no(prompt):
    clear_terminal()
    user_input = input(f'{prompt} (Y/N) \n')
    while user_input.upper() not in ["Y", "N", "YES", "NO"]:
        clear_terminal()
        print(f'You entered {user_input} Please enter "Y" or "N"')
        user_input = input(f'{prompt} (Y/N) \n')
    if user_input in ["Y", "YES"]:
        return True
    else:
        return False


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


# Add an additional prompt for request for download
def request_more_information(current_target_directory, current_file_name, current_sheet_name):
    target_directory = target_directory_prompt(current_target_directory)
    available_file_names(target_directory)
    file_name, sheet_name = file_name_prompt(current_file_name)
    available_sheet_names()
    sheet_name = sheet_name_prompt(current_sheet_name)
    return generate_document_list(target_directory, file_name, sheet_name)
