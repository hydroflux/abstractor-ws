import os
from time import sleep, time
from settings.general_functions import naptime


def check_for_download_error(browser):
    handles = browser.window_handles
    number_windows = len(handles)
    if number_windows > 1:
        window_before_click = handles[0]
        window_after_click = handles[1]
        browser.switch_to_window(window_after_click)
        if browser.title == 'Error':
            browser.close()
            browser.switch_to_window(window_before_click)
            return True
        else:
            browser.switch_to_window(window_before_click)


def wait_for_download(browser, document_directory, download_path, number_files):
    download_wait = True
    while not os.path.exists(download_path) and download_wait:
        sleep(1)
        check_for_download_error(browser)
        download_wait = False
        directory_files = os.listdir(document_directory)
        for file_name in directory_files:
            if file_name.endswith('.crdownload'):
                download_wait = True
        if len(directory_files) != number_files + 1:
            download_wait = True


def check_download_size(new_download_name, document_number):
    size = os.stat(new_download_name) == 0
    print(size)
    if size:
        os.remove(new_download_name)
        print(f'Failed to download document number {document_number}.')


def rename_download(document_directory, stock_download, document_number, download_path, new_download_name):
    if os.path.isfile(download_path):
        os.rename(stock_download, new_download_name)
        os.chdir(document_directory)
        check_download_size(new_download_name, document_number)
    else:
        raise ValueError("%s isn't a file!" % download_path)


def check_for_rename(browser, document_directory, number_files, document_number, new_download_name):
    rename_path = f'{document_directory}/{new_download_name}'
    # wait_for_download(browser, document_directory, rename_path, number_files)
    if os.path.isfile(rename_path):
        os.chdir(document_directory)
        check_download_size(new_download_name, document_number)
    else:
        raise ValueError("%s isn't a file!" % rename_path)


def update_download(browser, county, stock_download, document_directory, number_files, document_number):
    download_path = f'{document_directory}/{stock_download}'
    if wait_for_download(browser, document_directory, download_path, number_files):
        return False
    else:
        naptime()
        new_download_name = f'{county.prefix}-{document_number}.pdf'
        rename_download(document_directory, stock_download, document_number, download_path, new_download_name)
        naptime()
        check_for_rename(browser, document_directory, number_files, document_number, new_download_name)
        return True
