def multiple_documents_comment(document):
    return (f'Multiple documents located at {document.extrapolate_value()}'
            f' on the {document.county} recording website; Each of the {document.number_results}'
            f' documents has been listed, please review')


def record_comments(abstract, document):
    if document.number_results == 1:
        abstract.dataframe['Comments'].append('')
    elif document.number_results > 1:
        abstract.dataframe["Comments"].append(multiple_documents_comment(document))
    # if not document.image_available:
        #     no_document_image(dataframe, document)


def record_value(abstract, column, value):
    abstract.dataframe[column.title()].append(value)


def record_empty_values(abstract, columns):
    for column in columns:
        record_value(abstract, column, '')
