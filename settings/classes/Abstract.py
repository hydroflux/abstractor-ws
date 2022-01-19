class Abstract:
    def __init__(self, county, target_directory, download, review=False,
                 document_list=None):
        self.county = county
        self.target_directory = target_directory
        self.download = download
        self.review = review
        self.document_list = document_list
