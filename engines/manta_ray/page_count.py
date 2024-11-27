from selenium_utilities.locators import locate_element

# Same functionality as "swordfish"

def register_result_page_count(abstract, document, result):
    # page count container also contains information about the date of the document--
    # could be useful for determining when to update recording dates
    page_count_container = locate_element(result, "class", abstract.county.classes["Page Count"],
                                            "page count container", False, document=document)
    page_count_element = locate_element(page_count_container, "tags", abstract.county.tags["Page Count"],
                                        "page count element", False, document=document)[-1]
    return page_count_element.text.split(" ")[0]


def report_page_count(abstract, document, result_page_count):
    if document.number_results == 1:
        print(f'Document located at {document.extrapolate_value()} is {str(result_page_count)} page(s) '
              f'-- {str(abstract.total_page_count)} pages total '
              f'({abstract.list_remaining_documents(document)})')
    elif document.number_results > 1:
        print(f'Documents located at {document.extrapolate_value()} are a combined {str(result_page_count)} page(s) '
              f'-- {str(abstract.total_page_count)} pages total '
              f'({abstract.list_remaining_documents(document)})')


def register_page_count(abstract, document, result_rows):
    result_page_count = 0
    for result in result_rows:
        page_count_text = register_result_page_count(abstract, document, result)
        page_count = int(page_count_text)
        result_page_count += page_count
    abstract.total_page_count += result_page_count
    report_page_count(abstract, document, result_page_count)