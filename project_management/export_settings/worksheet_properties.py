from datetime import date

worksheet_properties = {
    'paper_size': 5,  # Legal
    'gridlines': 2,  # 2. Hide screen & printed gridlines
    'startrow': 5,
    'header_height': 120,
    'limitations_height': 15,
    'limitations_content': "LIMITATIONS",
    'disclaimer_height': 35,
    'footer_height': 15,
    'footer_content': f'Last Updated: {date.today()}',
    'hyperlink': 'Reception Number',
    'date_range': 'Recording Date',
    'breakpoint_start': 'Legal Description',
    'breakpoints': [
        {'title': 'NE', 'position': 1},
        {'title': 'NW', 'position': 1},
        {'title': 'SE', 'position': 1},
        {'title': 'SW', 'position': 2},
        {'title': 'WOL', 'position': 0}
    ],
    'custom_column_name': 'Legal',
    'datatype_content': {
        'primary_datatype_columns': [*range(0, 10), *range(14, 18)],
        'secondary_datatype_columns': [*range(10, 14)],
        'custom_datatype_column': 10
    },
    'column_formats': [
        {'column_name': 'Grantor', 'width': 45},
        {'column_name': 'Grantee', 'width': 45},
        {'column_name': 'Book', 'width': 8},
        {'column_name': 'Volume', 'width': 8},
        {'column_name': 'Page', 'width': 8},
        {'column_name': 'Reception Number', 'width': 15},
        {'column_name': 'Document Link', 'width': 15},
        {'column_name': 'Document Type', 'width': 20},
        {'column_name': 'Document Effective Date', 'width': 12},
        {'column_name': 'Recording Date', 'width': 12},
        {'column_name': 'NE', 'width': 7},
        {'column_name': 'NW', 'width': 7},
        {'column_name': 'SE', 'width': 7},
        {'column_name': 'SW', 'width': 7},
        {'column_name': 'Legal Description', 'width': 65},
        {'column_name': 'WOL', 'width': 8},
        {'column_name': 'Related Documents', 'width': 50},
        {'column_name': 'Comments', 'width': 50}
    ],
    'text_formats': {
        'large': {
            'font': 'Arial',
            'font_size': 16,
            'bold': True
        },
        'small': {
            'font': 'Arial',
            'font_size': 12,
            'bold': True
        },
        'header': {
            'text_wrap': True,
            'align': 'center',
            'valign': 'vcenter',
            'fg_color': '#91b7e1',
            'top': 2,
            'left': 2,
            'right': 2
        },
        'datatype': {
            'font': 'Arial',
            'font_size': 10,
            'bold': True,
            'text_wrap': True,
            'align': 'center',
            'valign': 'vcenter',
            'fg_color': '#BFBFBF',
            'border': 1
        },
        'body': {
            'font': 'Calibri',
            'font_size': 11,
            'text_wrap': True,
            'align': 'left',
            'valign': 'top',
            # 'border': 1
        },
        'border': {
            'border': 1
        },
        'limitations': {
            'font': 'Arial',
            'font_size': 10,
            'text_wrap': True,
            'fg_color': '#91b7e1',
            'bold': True,
            'align': 'center',
            'valign': 'top',
            'left': 2,
            'right': 2
        },
        'disclaimer':{
            'font': 'Arial',
            'font_size': 10,
            'text_wrap': True,
            'fg_color': '#91b7e1',
            'bold': False,
            'align': 'left',
            'valign': 'top',
            'bottom': 2,
            'left': 2,
            'right': 2
        },
        'footer': {
            'font': 'Arial',
            'font_size': 10,
            'text_wrap': True,
            'fg_color': '#91b7e1',
            'bold': True,
            'align': 'left',
            'valign': 'top',
            'top': 2,
            'left': 2,
            'right': 2,
            'border': 2
        },
        'hyperlink': {
            'font': 'Calibri',
            'font_size': 11,
            'text_wrap': True,
            'valign': 'top',
            'border': 1,
            'font_color': 'blue',
            'underline': 1
        },
        'no_record': {'bg_color': 'FCD5B4'},
        'multiple_documents': {'bg_color': 'CCC0DA'},
        'no_image': {'bg_color': 'B7DEE8'},
        'out_of_county': {'bg_color': 'C6E0B4'},
    },
    'conditional_formats': {
        'border_format_1': {
            'type': 'cell',
            'criteria': '>=',
            'value': 0,
            'format': {}
        },
        'border_format_2': {
            'type': 'cell',
            'criteria': '<',
            'value': 0,
            'format': {}
        },
        'no_record_format': {
            'type': 'formula',
            'criteria': '=LEFT($R5, 19)="No document located"',
            'format': {}
        },
        'multi_documents_format': {
            'type': 'formula',
            'criteria': '=LEFT($R5, 26)="Multiple documents located"',
            'format': {}
        },
        'no_image_format': {
            'type': 'formula',
            'criteria': '=LEFT($R5, 27)="No document image available"',
            'format': {}
        },
        'out_of_county_format': {
            'type': 'formula',
            'criteria': '=LEFT($R5, 26)="Document located out of county"',
            'format': {}
        },
    }
}