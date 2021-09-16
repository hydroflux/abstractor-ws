def no_image_comment(document):
    return f'No document image available at reception number "{document.reception_number}", please review'
# Add routes for document type
# needs to be done after book, volume, and page are added to the document class
