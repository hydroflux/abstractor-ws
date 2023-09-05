import os
from time import sleep

from selenium.common.exceptions import (NoSuchWindowException,
                                        WebDriverException)

from project_management.timers import medium_nap, naptime
from settings.general_functions import save_screenshot
from settings.invalid import no_download


def check_for_download_error(browser, windows):
    try:
        if browser.title == 'Error':
            browser.close()
            browser.switch_to.window(windows[0])
            return True
        else:
            # browser.close()  # Added this line on 06/05/22 to handle multiple windows in headless downloads
            # Instead of doing here wait for the download to finish and then close extra windows
            browser.switch_to.window(windows[0])
    except NoSuchWindowException:
        print('Encountered a "no such window exception" error while trying to close the download window, '
              'switching back to the original window.')
        browser.switch_to.window(windows[0])
    except WebDriverException:
        print('Encountered a "web driver exception" error while trying to close the download window, '
              'switching back to the original window.')
        save_screenshot(browser, 'check_for_download_error', 'WebDriverException')
        browser.switch_to.window(windows[0])


def check_browser_windows(browser):
    windows = browser.window_handles
    if len(windows) > 1:
        browser.switch_to.window(windows[1])
        if check_for_download_error(browser, windows):
            print("Error attempting to download document, please review.")
            return True


def check_for_download(browser, abstract, document, download_wait, count):
    count += 1
    if count == 250:
        input(f'Waiting for document "{document.target_name}" to be added into the document directory, '
              f'please press enter to continue...')
    if check_browser_windows(browser):
        return None
    sleep(2)  # Increase to 2 seconds if still having issues with no such window exception
    download_wait = False
    directory_files = os.listdir(abstract.document_directory)
    for file_name in directory_files:
        if file_name.endswith('.crdownload'):
            download_wait = True
    if len(directory_files) != abstract.document_directory_files + 1:
        download_wait = True
    return download_wait, count


def wait_for_download(browser, abstract, document):
    download_wait = True
    count = 0
    if document.alternate_download_path is not None:
        while (not (os.path.exists(document.download_path) or os.path.exists(document.alternate_download_path))
                and download_wait):
            download_wait, count = check_for_download(browser, abstract, document, download_wait, count)
            if download_wait is None:
                return False
    else:
        while not os.path.exists(document.download_path) and download_wait:
            download_wait, count = check_for_download(browser, abstract, document, download_wait, count)
            if download_wait is None:
                return False
    return True


# def wait_for_download(browser, abstract, document):
#     download_wait = True
#     count = 0
#     print("document.alternate", document.alternate_download_path)
#     while (not (os.path.exists(document.download_path) or os.path.exists(document.alternate_download_path))
#             and download_wait):
#         count += 1
#         if count == 250:
#             input(f'Waiting for document "{document.target_name}" to be added into the document directory, '
#                   f'please press enter to continue...')
#         check_browser_windows(browser)
#         sleep(2)  # Increase to 2 seconds if still having issues with no such window exception
#         download_wait = False
#         directory_files = os.listdir(abstract.document_directory)
#         for file_name in directory_files:
#             if file_name.endswith('.crdownload'):
#                 download_wait = True
#         if len(directory_files) != abstract.document_directory_files + 1:
#             download_wait = True


def check_download_size(new_download_name, document):
    size = os.stat(new_download_name) == 0
    if size:
        os.remove(new_download_name)
        print(f'Failed to download document number {document.reception_number}.')


def check_file_size(path):
    if os.path.isfile(path):
        return True
    else:
        # long_nap()  # Changed 12/03/21
        medium_nap()
        if os.path.isfile(path):
            return True
        else:
            return False


def prepare_file_for_download(abstract, document):
    if check_file_size(document.download_path):
        os.rename(document.download_value, document.target_name)
        check_download_size(document.target_name, document)
        return True
    elif os.path.isfile(f'{abstract.document_directory}/{document.target_name}'):
        check_download_size(document.target_name, document)
        return True
    else:
        # raise ValueError("%s isn't a file!" % document.download_path)
        print(f'Expected Download Path: {document.download_path}')
        if document.alternate_download_path:
            print(f'OR: {document.download_path}')
        print(f'Is File?: {abstract.document_directory}/{document.target_name}')
        print('Encountered an issue preparing file for download for '
              f'{document.extrapolate_value()}, trying again...')
        medium_nap()
        return False


def check_for_alternate(document):
    if document.alternate_download_path is not None and os.path.exists(document.alternate_download_path):
        document.download_value = document.alternate_download_value
        document.download_path = document.alternate_download_path


def rename_download(abstract, document):
    try:
        while not prepare_file_for_download(abstract, document):
            prepare_file_for_download(abstract, document)
    except FileNotFoundError:
        print(f'File not found, please review stock download '
              f'"{document.download_value}" & new file name "{document.target_name}"')
        input()


def check_for_rename(abstract, document):
    rename_path = f'{abstract.document_directory}/{document.target_name}'
    if os.path.isfile(rename_path):
        os.chdir(abstract.document_directory)
        check_download_size(document.target_name, document)
    else:
        raise ValueError("%s isn't a file!" % rename_path)


def reset_document_download_attributes(document):
    document.target_name = None


def update_download(browser, abstract, document):
    if wait_for_download(browser, abstract, document):
        naptime()
        check_for_alternate(document)
        rename_download(abstract, document)
        check_for_rename(abstract, document)
        abstract.report_document_download(document)
        reset_document_download_attributes(document)
        # Without a conditional, no_download will never be thrown???
        # no_download(abstract, document)
    else:
        print(f'No document image exists for '
              f'{document.extrapolate_value()}, please review.')
        no_download(abstract, document)
