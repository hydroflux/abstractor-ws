from datetime import datetime
from random import randint
from time import sleep

from settings.settings import abstraction_type

# Timeout / Wait Variables
timeout = randint(20, 30)
long_timeout = randint(120, 180)
short_timeout = randint(5, 10)


def naptime():
    sleep(randint(3, 4))  # Consider adding an additional second if running into issues while using naps


def micro_nap():
    if randint(0, 1) == 0:
        sleep(0.25)
    else:
        sleep(0.5)


def short_nap():
    sleep(randint(1, 2))


def medium_nap():
    sleep(randint(10, 20))


def long_nap():
    sleep(randint(30, 45))


def start_timer():
    return datetime.now()


def stop_timer(start_time):
    return datetime.now() - start_time


def update_user(abstract):
    if abstract.program in ["execute", "review", "download"]:
        if len(abstract.document_list) != 0:
            return f'{len(abstract.document_list)} documents imported for processing.'
        else:
            input(f'Something went wrong, the "{abstract.program}" search returned \
                  "{len(abstract.document_list)} for processing; Please review and press enter to continue...')
    elif abstract.program == 'legal':
        section, township, range, quarter = abstract.legal
        quarter = 'ALL' if quarter == '' else quarter
        return (f'Searching "Township {township} North - Range {range} West, Section {section}: {quarter}" '
                f'for any available documents in "{abstract.county}"...')
    elif abstract.program == 'name':
        return f'Searching "{abstract.county}" for any documents related to {abstract.search_name}...'
    else:
        input(f'Something went wrong, no user update available for a "{abstract.program}" program \
               "Please review and press enter to continue...')
        return ''


def start_program_timer(abstract):
    start_time = start_timer()
    print(f'\n{abstract.county} - {abstraction_type} started on: \n'
          f'{str(start_time.strftime("%B %d, %Y %H:%M:%S"))}\n'
          f'{update_user(abstract)}')
    return start_time
