class Project:
    def __init__(self, target_directory, dataframe, file_name=None,
                 writer=None, workbook=None, worksheet=None):
        self.target_directory = target_directory
        self.dataframe = dataframe
        self.file_name = file_name
        self.writer = writer
        self.workbook = workbook
        self.worksheet = worksheet
