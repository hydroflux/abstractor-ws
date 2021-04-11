import os
from time import sleep, time


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


def wait_for_download(browser, download_path):
    check_for_error = time() + 10
    while not os.path.exists(download_path):
        sleep(0.5)
        if time() > check_for_error:
            check_for_download_error(browser)


def check_download_size(new_download_name, document_number):
    size = os.stat(new_download_name) == 0
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


def update_download(browser, county, stock_download, document_directory, document_number):
    download_path = f'{document_directory}/{stock_download}'
    print("download path", download_path)
    print("update download document number", document_number)
    if wait_for_download(browser, download_path):
        print("download failed")
        return False
    else:
        print("download success")
        new_download_name = f'{county.prefix}-{document_number}.pdf'
        rename_download(document_directory, stock_download, document_number, download_path, new_download_name)
        return True
