def multiple_documents_comment(document):
    return (f'Multiple documents located at {document.extrapolate_value()}'
            f' on the {document.county} recording website; Each of the {document.number_results}'
            f' documents has been listed, please review')


def record_comments(abstract, document):
    pass


def record_invalid_value(abstract, column, value):
    abstract.dataframe[column.title()].append(value)
