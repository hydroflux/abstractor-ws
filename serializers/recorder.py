def multiple_documents_comment(document):
    return (f'Multiple documents located at {document.extrapolate_value()}'
            f' on the {document.county} recording website; Each of the {document.number_results}'
            f' documents has been listed, please review')


def record_comments(abstract, document):
    if document.number_results == 1:
        abstract.dataframe['Comments'].append('')
    elif document.number_results > 1:
        abstract.dataframe["Comments"].append(multiple_documents_comment(document))


def record_value(abstract, column, value):
    abstract.dataframe[column.title()].append(value)
