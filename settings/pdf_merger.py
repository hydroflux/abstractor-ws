from PyPDF2 import PdfFileMerger
import os


def sort_pdf_dictionary(dictionary):
    return [{key: sorted(value)} for key, value in dictionary.items()]


def create_pdf_dictionary(target_directory, pdf_dictionary={}):
    for pdf in os.listdir(target_directory):
        pdf_name = f'{pdf[:15]}.pdf'
        if pdf_name in pdf_dictionary:
            pdf_dictionary[pdf_name].append(pdf)
        else:
            pdf_dictionary[pdf_name] = [pdf]
    return sort_pdf_dictionary(pdf_dictionary)


def rename_pdfs(target_directory):
    pdf_dictionary = create_pdf_dictionary(target_directory)
    for item in pdf_dictionary.items():
        print(item)
