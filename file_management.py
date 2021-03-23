import os
from pandas import DataFrame


def create_folder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory ' + directory)


def create_dataframe(dictionary):
    dataframe = DataFrame(dictionary)
    print(dataframe)


def identify_county_information(county):
    return county_data.county_dictionary.get(county)


def rename_documents_in_directory(county, directory):
    os.chdir(directory)
    for pdf in os.listdir(directory):
        # Remove .DS_Store
        if pdf == '.DS_Store':
            full_path = os.path.join(directory, pdf)
            os.remove(full_path)
        elif pdf.startswith(county.prefix):
            continue
        else:
            new_document_name = county.prefix + '-' + pdf
            full_path = os.path.join(document_directory, pdf)
            os.rename(full_path, new_pdf_name)
            size = os.stat(new_pdf_name) == 0
            if size is True:
                os.remove(new_pdf_name)
                print('Failed to download reception number ' + pdf)