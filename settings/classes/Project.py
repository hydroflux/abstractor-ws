class Project:
    def __init__(self, target_directory, file_name=None,
                 writer=None, workbook=None, worksheet=None):
        self.target_directory = target_directory
        self.file_name = file_name
        self.writer = writer
        self.workbook = workbook
        self.worksheet = worksheet
