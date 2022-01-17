from settings.download_management import previously_downloaded


def execute_download(browser, document_directory, document):
    pass


def download_document(browser, document_directory, document):
    if previously_downloaded(document_directory, document):
        return True
    else:
        return execute_download(browser, document_directory, document)
