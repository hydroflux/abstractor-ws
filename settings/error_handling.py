def no_image_comment(document):
    no_image_comment = f'No document image available at reception number "{document.reception_number}", please review'
    print(no_image_comment)
    return no_image_comment
# Add routes for document type
# needs to be done after book, volume, and page are added to the document class
