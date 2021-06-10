from settings.file_management import extrapolate_document_value


def no_image_comment(document):
    return f'No document image available at {extrapolate_document_value(document)}, please review'
