from settings.file_management import access_document_directory

# The purposed of this script is to create hyperlinks for abstract exports
# it's "temporary" because the ideal situation will be to add hyperlinks directly into
# final product, but hit a roadblock which needs to be addressed later


def write_temporary_hyperlinks(county, target_directory, hyperlink_sheet):
    document_directory = access_document_directory(target_directory)
