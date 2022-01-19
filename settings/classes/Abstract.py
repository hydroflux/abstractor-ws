class Abstract:
    def __init__(self, county, target_directory, program_type, timer, download, review=False,
                 document_list=None):
        self.county = county
        self.target_directory = target_directory
        self.program_type = program_type
        self.timer = timer
        self.download = download
        self.review = review
        self.document_list = document_list


# - [ ] Put general button_ids on the 'abstract' class (login, logout, etc.)
# - [ ] Put urls on the abstract class
# - [ ] Update button_ids to button_attrs & similarly elsewhere
# - [ ] Add the 'download' trigger to the Document class (added here instead)

# From "Exports To Do"
# - [ ] Handle "ABSTRACTION TYPE" based on the "PROGRAM TYPE" rather than on a specific setting or user input
