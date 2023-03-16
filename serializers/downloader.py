import os
from time import time, sleep

from selenium.common.exceptions import JavascriptException

from settings.download_management import update_download
from settings.initialization import create_folder


def create_document_directory(target_directory):
    document_directory = f'{target_directory}/Documents'
    create_folder(document_directory)
    os.chdir(document_directory)
    return document_directory


def set_new_download_name(document):
    if document.target_name is None:
        if document.reception_number[0] == "-" or document.reception_number == "N/A":
            book, page = document.document_value()
            document.target_type = "book_and_page"
            return f'{document.county.prefix}-{book.zfill(4)}-{page.zfill(4)}.pdf'  # used for leopard
        else:
            document.target_type = "document_number"
            return f'{document.county.prefix}-{document.reception_number}.pdf'
    else:
        return document.target_name


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


# Could be a more generalized function imported into serializer
def close_download_window(browser):
    windows = browser.window_handles
    if len(windows) > 1:
        browser.switch_to.window(windows[1])
        browser.close()
        browser.switch_to.window(windows[0])


def set_downloaded_file_value(browser, document):  # updated 09/27/22
    if document.download_value is None:
        document.download_value = get_downloaded_file_name(browser)
        close_download_window(browser)


def set_download_path(browser, abstract, document):  # updated 09/27/22
    set_downloaded_file_value(browser, document)
    return f'{abstract.document_directory}/{document.download_value}'


def set_alternate_download_path(browser, abstract, document):
    if document.alternate_download_value:
        return f'{abstract.document_directory}/{document.alternate_download_value}'


def prepare_for_download(browser, abstract, document):
    abstract.document_directory = create_document_directory(abstract.target_directory)
    abstract.document_directory_files = len(os.listdir(abstract.document_directory))
    document.target_name = set_new_download_name(document)
    document.download_path = set_download_path(browser, abstract, document)
    document.alternate_download_path = set_alternate_download_path(browser, abstract, document)
    document.target_download_path = f'{abstract.document_directory}/{document.target_name}'


def is_duplicate(abstract, document, count=0):
    if document.number_results == 1:
        return True
    elif document.result_number > 0:
        document.is_duplicate = False
        if document.target_type == "document_number":
            reception_number_column = abstract.dataframe["Reception Number"]
            previous_reception_number = reception_number_column[-1]
            for reception_number in reception_number_column:
                if reception_number == previous_reception_number:
                    count += 1
                elif reception_number == f'{previous_reception_number}-{str(count)}':
                    count += 1
            if count > 1:
                print("naming count", count)
                reception_number_duplicate = f'{previous_reception_number}-{str(count - 1)}'
                abstract.dataframe["Reception Number"][-1] = reception_number_duplicate
                document.target_name = f'{document.county.prefix}-{reception_number_duplicate}.pdf'
                print("target name", document.target_name)
                return False
            else:
                return True
        elif document.target_type == "book_and_page":
            matching_book_indices = []
            book_column = abstract.dataframe["Book"]
            previous_book = book_column[-1]
            for book in book_column:
                if book == previous_book:
                    matching_book_indices.append(book_column.index(book))
                    count += 1
            if count > 1:
                index_match_count = 0
                page_column = abstract.dataframe["Page"]
                previous_page = page_column[-1]
                for page in page_column:
                    page_index = page_column.index(page)
                    if page == previous_page and page_index in matching_book_indices:
                        index_match_count += 1
                    elif page == f'{previous_page}-{str(count)}' and page_index in matching_book_indices:
                        index_match_count += 1
                if index_match_count > 1:
                    abstract.dataframe["Page"][-1] = f'{previous_page}-{str(count - 1)}'
                    document.target_name = f'{document.target_name[:-4]}-{str(count - 1)}.pdf'
        else:
            print(f'No duplication check created for document target type "{document.target_type}", '
                  f'please review "downloader" serializer for details.')
            input('Press enter to continue...')
    else:
        return True


def previously_downloaded(abstract, document):
    if os.path.exists(document.target_download_path):
        if is_duplicate(abstract, document):
            document.is_duplicate = True
            abstract.report_document_download(document)
            return True
        else:
            return False
    else:
        return False


def download_document(browser, abstract, document, execute_download):
    prepare_for_download(browser, abstract, document)
    if not previously_downloaded(abstract, document):
        execute_download(browser, abstract, document)
        # document.print_attributes()
        if document.image_available:
            update_download(browser, abstract, document)
