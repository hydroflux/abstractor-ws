class Project:
    def __init__(self, type, county, target_directory, dataframe, file_name, sheet_name,
                 writer=None, font_formats=None, workbook=None, worksheet=None):
        self.type = type
        self.county = county
        self.target_directory = target_directory
        self.dataframe = dataframe
        self.file_name = file_name
        self.sheet_name = sheet_name
        self.writer = writer
        self.font_formats = font_formats
        self.workbook = workbook
        self.worksheet = worksheet
