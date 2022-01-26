class Abstract:
    def __init__(self, type, county, target_directory, file_name, program,
                 headless, download, dataframe,
                 review=False, download_only=False, document_directory=None,
                 document_list=None, timer=None,
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


# - [ ] Put general button_ids on the 'abstract' class (login, logout, etc.)
# - [ ] Put urls on the abstract class
# - [ ] Update button_ids to button_attrs & similarly elsewhere

# From "Exports To Do"
# - [ ] Handle "ABSTRACTION TYPE" based on the "PROGRAM TYPE" rather than on a specific setting or user input
