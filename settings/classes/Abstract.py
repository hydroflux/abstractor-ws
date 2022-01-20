class Abstract:
    def __init__(self, county, target_directory, file_name, program,
                 headless, download, dataframe,
                 review=False, download_only=False, document_directory=None,
                 document_list=None, timer=None, abstraction=None,
                 search_name=None):
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
        self.abstraction = abstraction
        self.search_name = search_name


# - [ ] Put general button_ids on the 'abstract' class (login, logout, etc.)
# - [ ] Put urls on the abstract class
# - [ ] Update button_ids to button_attrs & similarly elsewhere
# - [ ] Add the 'download' trigger to the Document class (added here instead)

# From "Exports To Do"
# - [ ] Handle "ABSTRACTION TYPE" based on the "PROGRAM TYPE" rather than on a specific setting or user input
