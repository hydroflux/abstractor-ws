from PyPDF2 import PdfFileMerger, PdfFileReader
import os


def sort_pdf_dictionary(dictionary):
    [values.sort(key=lambda value: int(value[(value.rfind('-') + 1):])) for values in dictionary.values()]
    [values.insert(0, values.pop(values.index(key))) for key, values in dictionary.items()]
    return dictionary


def create_pdf_dictionary(target_directory, pdf_dictionary={}):
    for pdf in os.listdir(target_directory):
        if not pdf.endswith('.DS_Store'):
            # This is only going to work for rattlesnake for the time being--need to update naming syntax
            # pdf_name = f'{pdf[:15]}'  # Rattlesnake
            # if pdf_name in pdf_dictionary:
            #     pdf_dictionary[pdf_name].append(pdf[:-4])
            # else:
            #     pdf_dictionary[pdf_name] = [pdf[:-4]]
            # octopus
            pdf_name = f'{pdf[:13]}'
            if pdf_name in pdf_dictionary:
                pdf_dictionary[pdf_name].append(pdf[:-4])
            else:
                pdf_dictionary[pdf_name] = [pdf[:-4]]
    return sort_pdf_dictionary(pdf_dictionary)


def merge_pdfs(target_directory, pdf_dictionary):
    for name, pdfs in pdf_dictionary.items():
        print(name)
        merger = PdfFileMerger()
        [merger.append(PdfFileReader(f'{target_directory}/{pdf}.pdf', 'rb')) for pdf in pdfs]
        merger.write(f'{name}.pdf')
        merger.close()


def remove_original_files(target_directory):
    for file in os.listdir(target_directory):
        # if len(file) > 19 or file.endswith('.DS_Store'):  # Rattlesnake
        print(len(file))
        if len(file) > 17 or file.endswith('.DS_Store'):  # Octopus & # Platypus
            os.remove(file)


def rename_pdfs(target_directory):
    os.chdir(target_directory)
    pdf_dictionary = create_pdf_dictionary(target_directory)
    merge_pdfs(target_directory, pdf_dictionary)
    remove_original_files(target_directory)
