from PyPDF2 import PdfFileMerger, PdfFileReader
import os


def sort_pdf_dictionary(dictionary):
    return {key: sorted(value)[-1:] + sorted(value)[:-1] for key, value in dictionary.items()}


def create_pdf_dictionary(target_directory, pdf_dictionary={}):
    for pdf in os.listdir(target_directory):
        if not pdf.endswith('.DS_Store'):
            pdf_name = f'{pdf[:15]}.pdf'
            if pdf_name in pdf_dictionary:
                pdf_dictionary[pdf_name].append(pdf)
            else:
                pdf_dictionary[pdf_name] = [pdf]
    return sort_pdf_dictionary(pdf_dictionary)


def merge_pdfs(target_directory, pdf_dictionary):
    for name, pdfs in pdf_dictionary.items():
        merger = PdfFileMerger()
        [merger.append(PdfFileReader(f'{target_directory}/{pdf}', 'rb')) for pdf in pdfs]
        merger.write(f'{name}')
        merger.close()


def remove_original_files(target_directory):
    for file in os.listdir(target_directory):
        if len(file) > 19 or file.endswith('.DS_Store'):
            os.remove(file)


def rename_pdfs(target_directory):
    os.chdir(target_directory)
    pdf_dictionary = create_pdf_dictionary(target_directory)
    merge_pdfs(target_directory, pdf_dictionary)
    remove_original_files(target_directory)
