from datetime import datetime


def multiple_documents_comment(document):
    return (f'Multiple documents located at {document.extrapolate_value()}'
            f' on the {document.county} recording website; Each of the {document.number_results}'
            f' documents has been listed, please review')


def date_from_string(string):
    try:
        format = '%m/%d/%Y'
        return datetime.strptime(string, format).strftime(format)
    except ValueError:
        return string


def update_sentence_case_extras(text):
    return (text.replace("'S ", "'s ")
            .replace("1St ", "1st ")
            .replace("2Nd ", "2nd ")
            .replace("3Rd ", "3rd ")
            .replace("4Th ", "4th ")
            .replace("Llc ", "LLC ")
            .replace("Llp ", "LLP ")
            .replace("Ii ", "II ")
            .replace("Iii ", "III ")
            )


def title_strip(text):
    return text.title().strip()


def element_title_strip(element):
    return element.text.title().strip()


def remove_empty_list_items(list):
    while (" " in list):
        list.remove(" ")
    while ("" in list):
        list.remove("")
    return list


def list_to_string(list, newline=True):
    if newline:
        return "\n".join(list)
    else:
        return " ".join(list)


def record_value(abstract, column, value):
    if isinstance(value, str):
        value = update_sentence_case_extras(value)
    abstract.dataframe[column.title()].append(value)


def record_comments(abstract, document):
    if abstract.program in ['name', 'legal'] or document.number_results == 1:
        abstract.dataframe['Comments'].append('')
    elif document.number_results > 1:
        abstract.dataframe["Comments"].append(multiple_documents_comment(document))
    # if not document.image_available:
        #     no_document_image(dataframe, document)


def record_empty_values(abstract, columns):
    for column in columns:
        record_value(abstract, column, '')
