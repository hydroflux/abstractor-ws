from settings.initialization import convert_to_long_form


def number_to_letter(number):
    return chr(ord('@') + (number))


def set_title_format(project, font_format):
    project.worksheet.set_row(0, project.worksheet_properties['header_height'])
    project.worksheet.merge_range(f'A1:{project.last_column}1', '', font_format)


def create_range_message(dataframe, content):
    return f'From {convert_to_long_form(content["start_date"])} to {convert_to_long_form((content["end_date"]))} \n ({content["order"]})'


def write_title_content(project):
    content = project.worksheet_properties['header_content']
    content['county'] = f'{project.county}\n'
    range_message = create_range_message(project.dataframe, content)
    if project.client is not None and project.legal is not None:
        content['user'] = f'{project.client}\n'
        content['scope'] = f'{project.legal}\n'
    project.worksheet.write_rich_string(
        'A1',
        project.font_formats['large'], content['type'],
        project.font_formats['large'], content['user'],
        project.font_formats['small'], content['scope'],
        project.font_formats['small'], content['county'],
        project.font_formats['small'], range_message,
        project.font_formats['header']
    )


def add_title_row(project):
    set_title_format(project, project.font_formats['header'])
    write_title_content(project)


def add_limitations(project, font_format):
    project.worksheet.set_row(1, project.worksheet_properties['limitations_height'])
    project.worksheet.merge_range(f'A2:{project.last_column}2',
                                  project.worksheet_properties['limitations_content'],
                                  font_format)


def add_disclaimer(project, font_format):
    disclaimer_message = f'{project.disclaimer[0]}{project.county}{project.disclaimer[1]}'
    project.worksheet.set_row(2, project.worksheet_properties['disclaimer_height'])
    project.worksheet.merge_range(f'A3:{project.last_column}3', disclaimer_message, font_format)


def merge_primary_datatype_ranges(project, font_format):
    primary_range = project.worksheet_properties['datatype_content']['primary_datatype_columns']
    for column in primary_range:
        column_name = project.dataframe.columns[column]
        column_position = number_to_letter((column + 1))
        project.worksheet.merge_range(
            f'{column_position}4:{column_position}5',
            column_name,
            font_format
        )


def merge_custom_column(project, font_format):
    column = project.worksheet_properties['datatype_content']['custom_datatype_column']
    column_position_start = number_to_letter((column + 1))
    column_position_end = number_to_letter((column + 4))
    project.worksheet.merge_range(
        f'{column_position_start}4:{column_position_end}4',
        project.worksheet_properties['custom_column_name'],
        font_format
    )


def merge_secondary_datatype_ranges(project, font_format):
    primary_range = project.worksheet_properties['datatype_content']['secondary_datatype_columns']
    for column in primary_range:
        column_name = project.dataframe.columns[column]
        column_position = number_to_letter((column + 1))
        project.worksheet.write(
            f'{column_position}5',
            column_name,
            font_format
        )


def add_dataframe_headers(project, font_format):
    merge_primary_datatype_ranges(project, font_format)
    merge_custom_column(project, font_format)
    merge_secondary_datatype_ranges(project, font_format)


def set_worksheet_border(project, font_format):
    border_format_1 = project.worksheet_properties['conditional_formats']['border_format_1']
    border_format_2 = project.worksheet_properties['conditional_formats']['border_format_2']
    border_format_1['format'] = font_format
    border_format_2['format'] = font_format
    project.worksheet.conditional_format(project.worksheet_range, border_format_1)
    project.worksheet.conditional_format(project.worksheet_range, border_format_2)


def set_dataframe_format(project):
    body_format = project.font_formats['body']
    for column_format in project.worksheet_properties['column_formats']:
        if column_format.column_name in project.dataframe.columns:
            col_idx = project.dataframe.columns.get_loc(column_format.column_name)  # Get the 0-based index of the column
            col_letter = number_to_letter(col_idx + 1)  # Convert to 1-based index and then to letter
            column_range = f'{col_letter}:{col_letter}'
            project.worksheet.set_column(column_range, column_format.width, body_format)


def add_footer_row(project, font_format):
    footer_range = f'A{project.footer_row}:{project.last_column}{project.footer_row}'
    project.worksheet.set_row((project.last_row), project.worksheet_properties['footer_height'])
    project.worksheet.merge_range(footer_range, project.worksheet_properties['footer_content'], font_format)


def add_filter(project):
    project.worksheet.autofilter(f'A5:{project.last_column}{project.footer_row}')


# def add_watermark(project):
#     # Insert the watermark image in the header.
#     project.worksheet.set_header('&C&G', {'image_center': 'draft_watermark.png'})
#     project.worksheet.set_column('A:A', 50)
#     # worksheet.write('A1', 'Select Print Preview to see the watermark.')


def add_content(project):
    add_title_row(project)
    add_limitations(project, project.font_formats['limitations'])
    add_disclaimer(project, project.font_formats['disclaimer'])
    add_dataframe_headers(project, project.font_formats['datatype'])
    set_worksheet_border(project, project.font_formats['border'])
    set_dataframe_format(project)
    add_footer_row(project, project.font_formats['footer'])
    add_filter(project)
    # add_watermark(project)
