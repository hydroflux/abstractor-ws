import os
from time import sleep, time

from selenium.common.exceptions import (NoSuchWindowException, JavascriptException,
                                        WebDriverException)

from settings.general_functions import long_nap, naptime


def previously_downloaded(county, document_directory, document_number):
    document_download_path = f'{document_directory}/{county.prefix}-{document_number}.pdf'
    if os.path.exists(document_download_path):
        return True
    else:
        return False


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
        try:
            # get downloaded percentage
            download_percentage_script = ("return document.querySelector('downloads-manager')"
                                          ".shadowRoot.querySelector('#downloadsList downloads-item')"
                                          ".shadowRoot.querySelector('#progress').value")
            downloadPercentage = browser.execute_script(download_percentage_script)
            # check if downloadPercentage is 100 (otherwise the script will keep waiting)
            if downloadPercentage == 100:
                # return the file name once the download is completed
                download_name_script = ("return document.querySelector('downloads-manager')"
                                        ".shadowRoot.querySelector('#downloadsList downloads-item')"
                                        ".shadowRoot.querySelector('div#content  #file-link').text ")
                return browser.execute_script(download_name_script)
        except JavascriptException:  # Document already downloaded
            return browser.execute_script(download_name_script)
        sleep(1)
        if time() > endTime:
            break


# def stock_download_matches(document_directory, stock_download, count=0):
#     for document in os.listdir(document_directory):
#         if document.startswith(stock_download):
#             count += 1


def get_stock_download_path(document_directory, stock_download):
    for document in os.listdir(document_directory):
        if document.startswith(stock_download):
            return f'{document_directory}/{document}'


def set_download_path(browser, document_directory, stock_download, alt):
    if alt is None:
        return f'{document_directory}/{stock_download}', stock_download
    else:
        file = get_downloaded_file_name(browser)
        close_download_window(browser)
        # This will not work long term--this is a bandaid that needs surgery
        return f'{document_directory}/{file}', file


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


def wait_for_download(browser, document_directory, download_path, number_files):
    download_wait = True
    while not os.path.exists(download_path) and download_wait:
        check_browser_windows(browser)
        sleep(1)  # Increase to 2 seconds if still having issues with no such window exception
        download_wait = False
        directory_files = os.listdir(document_directory)
        for file_name in directory_files:
            if file_name.endswith('.crdownload'):
                download_wait = True
        if len(directory_files) != number_files + 1:
            download_wait = True


def check_download_size(new_download_name, document_number):
    size = os.stat(new_download_name) == 0
    if size:
        os.remove(new_download_name)
        print(f'Failed to download document number {document_number}.')


def check_file_size(download_path):
    if os.path.isfile(download_path):
        return True
    else:
        long_nap()
        if os.path.isfile(download_path):
            return True
        else:
            return False


def prepare_file_for_download(document_directory, current_download, document_number, download_path, new_download_name):
    if check_file_size(download_path):
        print('prepare', current_download, new_download_name)
        os.rename(current_download, new_download_name)
        os.chdir(document_directory)
        check_download_size(new_download_name, document_number)
    else:
        raise ValueError("%s isn't a file!" % download_path)


def rename_download(document_directory, current_download, document_number, download_path, new_download_name):
    try:
        print('download path', download_path)
        print('current download', current_download)
        prepare_file_for_download(document_directory, current_download, document_number, download_path, new_download_name)
    except FileNotFoundError:
        print(f'File not found, please review stock download {current_download} & new file name {new_download_name}')


def check_for_rename(browser, document_directory, number_files, document_number, new_download_name):
    rename_path = f'{document_directory}/{new_download_name}'
    # wait_for_download(browser, document_directory, rename_path, number_files)
    if os.path.isfile(rename_path):
        os.chdir(document_directory)
        check_download_size(new_download_name, document_number)
    else:
        raise ValueError("%s isn't a file!" % rename_path)


def update_download(browser, county, stock_download, document_directory, number_files, document_number, alt=None):
    download_path, current_download = set_download_path(browser, document_directory, stock_download, alt)
    if wait_for_download(browser, document_directory, download_path, number_files):
        return False
    else:
        naptime()
        new_download_name = f'{county.prefix}-{document_number}.pdf'
        rename_download(document_directory, current_download, document_number, download_path, new_download_name)
        # naptime()
        check_for_rename(browser, document_directory, number_files, document_number, new_download_name)
        return True
