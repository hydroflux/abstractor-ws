def add_no_record_format(project):
    no_record_format = project.worksheet_properties['conditional_formats']['no_record_format']
    no_record_format['format'] = project.font_formats['no_record']
    project.worksheet.conditional_format(project.worksheet_range, no_record_format)


def add_multiple_document_format(project):
    multi_documents_format = project.worksheet_properties['conditional_formats']['multi_documents_format']
    multi_documents_format['format'] = project.font_formats['multiple_documents']
    project.worksheet.conditional_format(project.worksheet_range, multi_documents_format)


def add_no_document_image_format(project):
    no_document_image_format = project.worksheet_properties['conditional_formats']['no_image_format']
    no_document_image_format['format'] = project.font_formats['no_image']
    project.worksheet.conditional_format(project.worksheet_range, no_document_image_format)


def add_out_of_county_format(project):
    font_format = project.font_formats['out_of_county']
    out_of_county_format = project.worksheet_properties['conditional_formats']['out_of_county_format']
    out_of_county_format['format'] = font_format
    project.worksheet.conditional_format(project.worksheet_range, out_of_county_format)


def add_conditional_formatting(project):
    add_no_record_format(project)
    add_multiple_document_format(project)
    add_no_document_image_format(project)
    add_out_of_county_format(project)
