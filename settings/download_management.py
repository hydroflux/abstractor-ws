import os
from time import sleep, time

from selenium.common.exceptions import (NoSuchWindowException, JavascriptException,
                                        WebDriverException)
from settings.file_management import document_downloaded

from settings.general_functions import medium_nap, naptime


def build_previous_download_path(abstract, document):
    if document.new_name is None:
        return f'{abstract.document_directory}/{document.county.prefix}-{document.reception_number}.pdf'
    else:
        return f'{abstract.document_directory}/{document.new_name}'


def is_duplicate(abstract, document, count=0):
    if document.number_results == 1:
        return False
    elif document.result_number > 0 and document.type == "document_number":
        for element in abstract.dataframe["Reception Number"]:
            if element == abstract.dataframe["Reception Number"][-1]:
                count += 1
            elif element == f'{abstract.dataframe["Reception Number"][-1]}-{str(count)}':
                count += 1
        if count > 1:
            abstract.dataframe["Reception Number"][-1] = f'{abstract.dataframe["Reception Number"][-1]}-{str(count - 1)}'
            document.new_name = f'{document.county.prefix}-{document.reception_number}-{str(count - 1)}.pdf'
            return True
        else:
            return False
    else:
        return False


def previously_downloaded(abstract, document):
    document_download_path = build_previous_download_path(abstract, document)
    if os.path.exists(document_download_path):
        if is_duplicate(abstract, document):
            # print statement about duplicate
            return False
        else:
            document_downloaded(abstract, document)
            return True
    else:
        return False


# def download_document(browser, abstract, document):
#     prepare_for_download(abstract, document)
#     if previously_downloaded(abstract, document):
#         if abstract.duplicate_review_and_update(document):
#             return True
#     execute_download(browser, abstract, document)


def close_download_window(browser):
    windows = browser.window_handles
    if len(windows) > 1:
        browser.switch_to.window(windows[1])
        browser.close()
        browser.switch_to.window(windows[0])


def get_downloaded_file_name(browser, wait_time=300):
    browser.execute_script("window.open()")
    # switch to new tab
    browser.switch_to.window(browser.window_handles[-1])
    # navigate to chrome downloads
    browser.get('chrome://downloads')
    # define the endTime
    endTime = time() + wait_time
    while True:
        download_percentage_script = ("return document.querySelector('downloads-manager')"
                                      ".shadowRoot.querySelector('#downloadsList downloads-item')"
                                      ".shadowRoot.querySelector('#progress').value")
        download_name_script = ("return document.querySelector('downloads-manager')"
                                ".shadowRoot.querySelector('#downloadsList downloads-item')"
                                ".shadowRoot.querySelector('div#content  #file-link').text ")
        try:
            # get downloaded percentage
            downloadPercentage = browser.execute_script(download_percentage_script)
            # check if downloadPercentage is 100 (otherwise the script will keep waiting)
            if downloadPercentage == 100:
                # return the file name once the download is completed
                return browser.execute_script(download_name_script)
        except JavascriptException:  # Document already downloaded
            return browser.execute_script(download_name_script)
        sleep(1)
        if time() > endTime:
            break


def set_new_download_name(document):
    if document.new_name is None:
        document.new_name = f'{document.county.prefix}-{document.reception_number}.pdf'


def set_download_path_and_name_values(browser, abstract, document):
    set_new_download_name(document)
    if document.download_value is not None:
        document.download_path = f'{abstract.document_directory}/{document.download_value}'
    else:
        document.download_value = get_downloaded_file_name(browser)
        close_download_window(browser)
        document.download_path = f'{abstract.document_directory}/{document.download_value}'


def check_for_download_error(browser, windows):
    try:
        if browser.title == 'Error':
            browser.close()
            browser.switch_to.window(windows[0])
            return True
        else:
            browser.switch_to.window(windows[0])
    except NoSuchWindowException:
        print('Encountered a "no such window exception" error while trying to close the download window, '
              'switching back to the original window.')
        browser.switch_to.window(windows[0])
    except WebDriverException:
        print('Encountered a "web driver exception" error while trying to close the download window, '
              'switching back to the original window.')
        browser.switch_to.window(windows[0])


def check_browser_windows(browser):
    windows = browser.window_handles
    if len(windows) > 1:
        browser.switch_to.window(windows[1])
        check_for_download_error(browser, windows)


def wait_for_download(browser, abstract, document):
    download_wait = True
    while not os.path.exists(document.download_path) and download_wait:
        check_browser_windows(browser)
        sleep(1)  # Increase to 2 seconds if still having issues with no such window exception
        download_wait = False
        directory_files = os.listdir(abstract.document_directory)
        for file_name in directory_files:
            if file_name.endswith('.crdownload'):
                download_wait = True
        if len(directory_files) != abstract.document_directory_files + 1:
            download_wait = True


def check_download_size(new_download_name, document):
    size = os.stat(new_download_name) == 0
    if size:
        os.remove(new_download_name)
        print(f'Failed to download document number {document.reception_number}.')


def check_file_size(download_path):
    if os.path.isfile(download_path):
        return True
    else:
        # long_nap()  # Changed 12/03/21
        medium_nap()
        if os.path.isfile(download_path):
            return True
        else:
            return False


def prepare_file_for_download(abstract, document):
    if check_file_size(document.download_path):
        os.rename(document.download_value, document.new_name)
        check_download_size(document.new_name, document)
        return True
    elif os.path.isfile(f'{abstract.document_directory}/{document.document.new_name}'):
        check_download_size(document.new_name, document)
        return True
    else:
        # raise ValueError("%s isn't a file!" % document.download_path)
        print('Encountered an issue preparing file for download for '
              f'{document.extrapolate_value()}, trying again...')
        medium_nap()
        return False


def rename_download(abstract, document):
    try:
        while not prepare_file_for_download(abstract.document_directory, document):
            prepare_file_for_download(abstract.document_directory, document)
    except FileNotFoundError:
        print(f'File not found, please review stock download '
              f'"{document.download_value}" & new file name "{document.new_name}"')
        input()


def check_for_rename(abstract, document):
    rename_path = f'{abstract.document_directory}/{document.new_name}'
    if os.path.isfile(rename_path):
        os.chdir(abstract.document_directory)
        check_download_size(document.new_name, document)
    else:
        raise ValueError("%s isn't a file!" % rename_path)


def update_download(browser, abstract, document):
    set_download_path_and_name_values(browser, abstract, document)
    wait_for_download(browser, abstract, document)
    naptime()
    rename_download(abstract, document)
    check_for_rename(abstract, document)
    document_downloaded(abstract, document)
    # Without a conditional, no_download will never be thrown???
    # no_download(abstract, document)
