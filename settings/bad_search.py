from .variables import search_errors

def record_bad_search(dataframe, document_number):
    bad_search_message = f'No document found at reception number {document_number}'
    dataframe["Grantor"].append(search_errors[0])
    dataframe["Grantee"].append(search_errors[0])
    dataframe["Book"].append(search_errors[2])
    dataframe["Page"].append(search_errors[2])
    dataframe["Reception Number"].append(document_number)
    dataframe["Document Type"].append(search_errors[0])
    dataframe["Recording Date"].append(search_errors[1])
    dataframe["Legal"].append(search_errors[2])
    dataframe["Related Documents"].append(search_errors[2])
    dataframe["Comments"].append(bad_search_message)
