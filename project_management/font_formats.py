def generate_font_formats(project):
    return {
        'large': project.workbook.add_format(project.text_formats['large']),
        'small': project.workbook.add_format(project.text_formats['small']),
        'header': project.workbook.add_format(project.text_formats['header']),
        'datatype': project.workbook.add_format(project.text_formats['datatype']),
        'body': project.workbook.add_format(project.text_formats['body']),
        'border': project.workbook.add_format(project.text_formats['border']),
        'limitations': project.workbook.add_format(project.text_formats['limitations']),
        'disclaimer': project.workbook.add_format(project.text_formats['disclaimer']),
        'footer': project.workbook.add_format(project.text_formats['footer']),
        'no_record': project.workbook.add_format(project.text_formats['no_record']),
        'multiple_documents': project.workbook.add_format(project.text_formats['multiple_documents']),
        'no_image': project.workbook.add_format(project.text_formats['no_image']),
        'out_of_county': project.workbook.add_format(project.text_formats['out_of_county'])
    }
