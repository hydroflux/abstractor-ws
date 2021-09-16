def no_image_comment(document):
    no_image_comment = f'No document image available at {document.extrapolate_value()}, please review'
    print(no_image_comment)
    return no_image_comment
