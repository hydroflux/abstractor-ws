class Project:
    def __init__(self, type, target_directory, dataframe, file_name,
                 writer=None, workbook=None, worksheet=None):
        self.type = type
        self.target_directory = target_directory
        self.dataframe = dataframe
        self.file_name = file_name
        self.writer = writer
        self.workbook = workbook
        self.worksheet = worksheet
