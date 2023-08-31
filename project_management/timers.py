from datetime import datetime
from random import randint
from time import sleep

from settings.county_variables.general import abstraction_type

# Timeout / Wait Variables
timeout = randint(20, 30)
long_timeout = randint(120, 180)
short_timeout = randint(5, 10)
micro_timeout = randint(3, 5)


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
    # sleep(randint(10, 20))
    sleep(randint(15, 30))


def long_nap():
    sleep(randint(30, 45))


def combination_nap(naps):
    for nap in naps:
        if nap == "micro_nap":
            micro_nap()
        elif nap == "short_nap":
            short_nap()
        elif nap == "naptime":
            naptime()
        elif nap == "medium_nap":
            medium_nap()
        elif nap == "long_nap":
            long_nap()


def nap(type=None):
    if type is None:
        naptime()
    else:
        if type == "micro":
            micro_nap()
        elif type == "short":
            short_nap()
        elif type == "naptime":
            naptime()
        elif type == "medium":
            medium_nap()
        elif type == "long":
            long_nap()


def start_timer():
    return datetime.now()


def stop_timer(start_time):
    return datetime.now() - start_time


# def stop_after(action, number_seconds):
#     fail = time() + number_seconds
#     while time() < fail:
#         try:
#             action
#             return True
#         except WebDriverException:
#             micro_nap()
#     if time() > fail:
#         return False


def update_user(abstract):
    if abstract.program in ["execute", "review", "download", "register_page_count"]:
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
