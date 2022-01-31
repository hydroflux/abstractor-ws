from datetime import datetime


class Abstract:
    def __init__(self, type, county, target_directory, file_name, program,
                 headless, download, dataframe,
                 review=False, download_only=False, download_type=None,
                 document_directory=None, document_list=None, timer=None,
                 search_name=None,
                 document_directory_files=None):
        self.type = type
        self.county = county
        self.target_directory = target_directory
        self.file_name = file_name
        self.program = program
        self.headless = headless
        self.download = download
        self.dataframe = dataframe
        self.review = review
        self.download_only = download_only
        self.download_type = download_type
        self.document_directory = document_directory
        self.document_list = document_list
        self.timer = timer
        self.search_name = search_name
        self.document_directory_files = document_directory_files

    def drop_last_entry(self):
        self.dataframe["Grantor"].pop()
        self.dataframe["Grantee"].pop()
        self.dataframe["Book"].pop()
        self.dataframe["Volume"].pop()
        self.dataframe["Page"].pop()
        self.dataframe["Reception Number"].pop()
        self.dataframe["Document Link"].pop()
        self.dataframe["Document Type"].pop()
        self.dataframe["Effective Date"].pop()
        self.dataframe["Recording Date"].pop()
        self.dataframe["Legal"].pop()
        self.dataframe["Related Documents"].pop()
        self.dataframe["Comments"].pop()

    def check_last_document(self, document):
        if len(self.dataframe['Reception Number']) >= 2:
            if document.index_number == self.document_list[self.document_list.index(document) - 1].index_number and \
              document.result_number == 0:
                if self.dataframe["Grantor"][-1] == self.dataframe["Grantor"][-2] and \
                  self.dataframe["Grantee"][-1] == self.dataframe["Grantee"][-2] and \
                  self.dataframe["Book"][-1] == self.dataframe["Book"][-2] and \
                  self.dataframe["Volume"][-1] == self.dataframe["Volume"][-2] and \
                  self.dataframe["Page"][-1] == self.dataframe["Page"][-2] and \
                  self.dataframe["Reception Number"][-1] == self.dataframe["Reception Number"][-2] and \
                  self.dataframe["Document Link"][-1] == self.dataframe["Document Link"][-2] and \
                  self.dataframe["Document Type"][-1] == self.dataframe["Document Type"][-2] and \
                  self.dataframe["Effective Date"][-1] == self.dataframe["Effective Date"][-2] and \
                  self.dataframe["Recording Date"][-1] == self.dataframe["Recording Date"][-2] and \
                  self.dataframe["Legal"][-1] == self.dataframe["Legal"][-2] and \
                  self.dataframe["Related Documents"][-1] == self.dataframe["Related Documents"][-2] and \
                  self.dataframe["Comments"][-1] == self.dataframe["Comments"][-2]:
                    self.drop_last_entry()

    def check_length(self):
        grantors = len(self.dataframe["Grantor"])
        grantees = len(self.dataframe["Grantee"])
        books = len(self.dataframe["Book"])
        volumes = len(self.dataframe["Volume"])
        pages = len(self.dataframe["Page"])
        reception_numbers = len(self.dataframe["Reception Number"])
        document_links = len(self.dataframe["Document Link"])
        document_types = len(self.dataframe["Document Type"])
        effective_dates = len(self.dataframe["Effective Date"])
        recording_dates = len(self.dataframe["Recording Date"])
        legals = len(self.dataframe["Legal"])
        related_documents = len(self.dataframe["Related Documents"])
        comments = len(self.dataframe["Comments"])
        if (grantors == grantees == books == volumes == pages
                == reception_numbers == document_links == document_types
                == effective_dates == recording_dates == legals
                == related_documents == comments):
            pass
        else:
            print("Grantors: ", grantors)
            print("Grantees: ", grantees)
            print("Books: ", books)
            print("Volumes: ", volumes)
            print("Pages: ", pages)
            print("Reception Numbers: ", reception_numbers)
            print("Document Links: ", document_links)
            print("Document Types: ", document_types)
            print("Effective Dates: ", effective_dates)
            print("Recording Dates: ", recording_dates)
            print("Legals: ", legals)
            print("Related Documents: ", related_documents)
            print("Comments: ", comments)

    def last_document(self, document):
        return self.document_list[self.document_list.index(document) - 1]

    def account_for_number_results(self, document):
        if document.number_results > 1:
            return f' - {document.number_results} results found for {document.extrapolate_value()}'
        else:
            return ''

    def remaining_documents(self, document):
        return len(self.document_list) - self.document_list.index(document) - 1

    def list_remaining_documents(self, document):
        return f'{self.remaining_documents(document)} documents remaining'

    def report_execution_time(self, time):
        return str(datetime.now() - time)

    def document_found(self, document):
        if self.review is False:
            print('Document located at '
                  f'{document.extrapolate_value()} recorded'
                  f'{self.account_for_number_results(document)}, '
                  f'{self.list_remaining_documents(document)} '
                  f'({self.report_execution_time(document.start_time)})')
        elif self.review is True:
            input(f'Document located at {document.extrapolate_value()} found'
                  f'{self.account_for_number_results(document)}, '
                  'please review & press enter to continue... '
                  f'({self.list_remaining_documents(document)}) '
                  f'({self.report_execution_time(document.start_time)})')
        # elif alt == "download":
        #     print('Document located at '
        #           f'{document.extrapolate_value()} downloaded, '
        #           f'{list_remaining_documents(document_list, document)} '
        #           f'({report_execution_time(start_time)})')

    def no_document_found(self, document):
        if self.review is False:
            print('No document found at '
                  f'{document.extrapolate_value()}, '
                  f'{self.list_remaining_documents(document)} '
                  f'({self.report_execution_time(document.start_time)})')
        elif self.review is True:
            input(f'No document found at {document.extrapolate_value()}, '
                  'please review & press enter to continue... '
                  f'({self.list_remaining_documents(document)}) '
                  f'({self.report_execution_time(document.start_time)})')

    def document_downloaded(self, document):
        print(f'Document located at '
              f'{document.extrapolate_value()} downloaded'
              f'{self.account_for_number_results(document)}, '
              f'{self.list_remaining_documents(self, document)} '
              f'{"(" + (self.report_execution_time(document.start_time)) + ")" if self.download_only else ""}')

    def no_document_downloaded(self, document):
        print(f'Unable to download document at '
              f'{document.extrapolate_value()}'
              f'{self.account_for_number_results(document)}, '
              f'({self.list_remaining_documents(self, document)}) '
              f'{"(" + (self.report_execution_time(document.start_time)) + ")" if self.download_only else ""}')

    def stop_program_timer(self):
        print(f'Total Run Time: {self.report_execution_time(self.timer)}')


# - [ ] Put general button_ids on the 'abstract' class (login, logout, etc.)
# - [ ] Put urls on the abstract class
# - [ ] Update button_ids to button_attrs & similarly elsewhere

# From "Exports To Do"
# - [ ] Handle "ABSTRACTION TYPE" based on the "PROGRAM TYPE" rather than on a specific setting or user input
