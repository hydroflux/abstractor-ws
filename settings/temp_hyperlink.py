import os

# The purposed of this script is to create hyperlinks for abstract exports
# it's "temporary" because the ideal situation will be to add hyperlinks directly into
# final product, but hit a roadblock which needs to be addressed later


def drop_ds_store(file):
    if file.endswith('.DS_Store'):
        os.remove(file)
        return True


def write_hyperlink_url():
    pass


def write_temporary_hyperlinks(county, document_directory, hyperlink_sheet, hyperlink_format):
    for file in sorted(os.listdir(document_directory)):
        if not drop_ds_store(file):
            write_hyperlink_url()
