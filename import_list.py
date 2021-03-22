import pandas as pd

def import_excel_document(file_path, sheet_name):
    excel = pd.read_excel(file_path, sheet_name)
    return excel.values.flatten().tolist()

def generate_document_list(target_directory, file_name, sheet_name):
    file_path = f'{target_directory}/{file_name}.xlsx'
    return import_excel_document(file_path, sheet_name)
    