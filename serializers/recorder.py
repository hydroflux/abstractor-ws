def record_comments(abstract, document):
    pass


def record_invalid_value(abstract, column, value):
    abstract.dataframe[column.title()].append(value)
