from project_management.timers import short_nap
from selenium_utilities.locators import locate_element_by_class_name, locate_element_by_tag_name, locate_elements_by_class_name, locate_elements_by_tag_name
from serializers.recorder import record_comments, record_empty_values, record_value
import time
from selenium.webdriver.remote.webdriver import WebDriver
from classes.Abstract import Abstract
from classes.Document import Document


def wait_for_page_to_load(browser: WebDriver, abstract: Abstract, document: Document) -> None:
    """
    Wait for the page to load by checking for the presence of the indexing information container.
    If the page does not load within 30 seconds, refresh the browser and reset the timer.
    If the page does not load after 2 minutes (4 attempts), prompt the user to review.

    Args:
        browser (WebDriver): The WebDriver instance.
        abstract (Abstract): The abstract information.
        document (Document): The document information.
    """
    count = 0
    start_time = time.time()
    while True:
        document_present = locate_element_by_class_name(browser, abstract.county.record["Indexing Information"], "indexing information", quick=True, document=document)
        if document_present is not None:
            break
        if time.time() - start_time > 30:
            print("Page did not load within 30 seconds. Refreshing the browser...")
            browser.refresh()
            start_time = time.time()  # Reset the start time after refreshing
            count += 1
        if count == 4:
            input("The page did not load after 2 minutes. Please review and press enter to continue.")


def click_show_elements(browser, abstract, document):
    """
    Click on elements that match the specified criteria if their text starts with the specified text.

    Args:
        browser (WebDriver): The WebDriver instance.
        abstract (Abstract): The abstract information.
        document (Document): The document information.
    """
    while True:
        show_elements = locate_elements_by_class_name(browser, abstract.county.record["Show All Elements"],
                                                      "show elements", False, document, quick=True, timeout=1)
        if not show_elements:
            break
        clicked = False
        for element in show_elements:
            if element.text.startswith(abstract.county.record["Show Element Text"]):
                element.click()
                clicked = True
        if not clicked:
            break


def record_indexing_information(browser, abstract, document):
    """
    Record the indexing information from the web page.

    Args:
        browser (WebDriver): The WebDriver instance.
        abstract (Abstract): The abstract information.
        document (Document): The document information.
    """
    indexing_information_container = locate_element_by_class_name(browser, abstract.county.record["Indexing Information"],
                                                                  "indexing information", False, document)
    indexing_information_items = locate_elements_by_class_name(indexing_information_container, abstract.county.record["Indexing Items"],
                                                               "indexing information items", False, document)
    for item in indexing_information_items:
        item_text = item.text
        if item_text.startswith(abstract.county.record["Reception Number Text"]):
            reception_number = item_text.split("\n")[1]
            if document.reception_number and reception_number != document.reception_number:
                input(f"Reception number mismatch: expected {document.reception_number} from description link, "
                      f"found {reception_number} on the result page. Please review and press enter to continue.")
                return  # Skip recording for this document
            record_value(abstract, 'reception number', reception_number)
        elif item_text.startswith(abstract.county.record["Book Text"]):
            book = item_text.split("\n")[1]
            record_value(abstract, 'book', book)
        elif item_text.startswith(abstract.county.record["Page Text"]):
            page = item_text.split("\n")[1]
            record_value(abstract, 'page', page)
        elif item_text.startswith(abstract.county.record["Number Pages Text"]):
            number_pages = item_text.split("\n")[1]
            abstract.total_page_count += int(number_pages)
        elif item_text.startswith(abstract.county.record["Recording Date Text"]):
            recording_date_text = item_text.split("\n")[1]
            recording_date = recording_date_text.split(" ")[0]
            record_value(abstract, 'recording date', recording_date)
        else:
            input("Unexpected indexing information item. Please review and press enter to continue.")


def record_document_type(browser, abstract, document):
    """
    Record the document type from the web page.

    Args:
        browser (WebDriver): The WebDriver instance.
        abstract (Abstract): The abstract information.
        document (Document): The document information.
    """
    document_type_field = locate_element_by_class_name(browser, abstract.county.record["Document Type"],
                                                       "document type", False, document)
    document_type = document_type_field.text.title()
    record_value(abstract, 'document type', document_type)


def record_parties(browser, abstract, document):
    """
    Record the parties (Grantor and Grantee) from the web page.

    Args:
        browser (WebDriver): The WebDriver instance.
        abstract (Abstract): The abstract information.
        document (Document): The document information.
    """
    parties_container = locate_elements_by_class_name(browser, abstract.county.record["Additional Information"],
                                                      "parties container", False, document)[0]
    grantors = []
    grantees = []
    if parties_container:
        party_items_container = locate_element_by_class_name(parties_container, abstract.county.record["Parties"],
                                                             "party items container", False, document)
        text_elements = locate_elements_by_class_name(party_items_container, abstract.county.record["Party Item Text"],
                                                      "party item text", False, document)
        label_elements = locate_elements_by_class_name(party_items_container, abstract.county.record["Party Item Label"],
                                                       "party item label", False, document)
        for text_element, label_element in zip(text_elements, label_elements):
            label_text = label_element.text
            text_value = text_element.text
            if label_text == abstract.county.record["Grantor Text"]:
                grantor = text_value.title()
                grantors.append(grantor)
            elif label_text == abstract.county.record["Grantee Text"]:
                grantee = text_value.title()
                grantees.append(grantee)
            else:
                input(f"Unexpected party label: {label_text}. Please review and press enter to continue.")
        record_value(abstract, 'grantor', "\n".join(grantors))
        record_value(abstract, 'grantee', "\n".join(grantees))
    else:
        input("No parties found. Please review and press enter to continue.")


def record_related_documents(browser, abstract, document):
    """
    Record the related documents (Marginal References) from the web page.

    Args:
        browser (WebDriver): The WebDriver instance.
        abstract (Abstract): The abstract information.
        document (Document): The document information.
    """
    related_documents_container = locate_elements_by_class_name(browser, abstract.county.record["Additional Information"],
                                                                "related documents container", False, document)[1]
    related_documents = []
    if related_documents_container:
        if "No marginal references found." in related_documents_container.text:
            record_value(abstract, 'related documents', "")
        else:
            related_document_items = locate_elements_by_class_name(related_documents_container, abstract.county.record["Related Documents"],
                                                                   "related document items", False, document)
            for item in related_document_items:
                related_documents.append(item.text)
            record_value(abstract, 'related documents', "\n".join(related_documents))
    else:
        input("No related documents found. Please review and press enter to continue.")


def record_legal(browser, abstract, document):
    """
    Record the legal description from the web page.

    Args:
        browser (WebDriver): The WebDriver instance.
        abstract (Abstract): The abstract information.
        document (Document): The document information.
    """
    legal_container = locate_elements_by_class_name(browser, abstract.county.record["Additional Information"],
                                                    "legal container", False, document)[2]
    legal_descriptions = []
    if legal_container:
        if legal_container.text == abstract.county.record["No Legal Information Found"]:
            record_value(abstract, 'legal', "")
            return
        table = locate_element_by_class_name(legal_container, abstract.county.record["Legal Table"], "legal table", False, document)
        headers = [header.text for header in locate_elements_by_tag_name(table, abstract.county.record["Legal Table Header"],
                                                                         "legal table headers", False, document)]
        table_body = locate_element_by_tag_name(table, abstract.county.record["Legal Table Body"], "legal table body")
        rows = locate_elements_by_tag_name(table_body, abstract.county.record["Legal Rows"], "legal table rows")
        for row in rows:
            row_descriptions = []
            cells = locate_elements_by_tag_name(row, abstract.county.record["Legal Row Data"], "legal table cells")
            for i, cell in enumerate(cells):
                if cell.text != "N/A" and cell.text != "SEE RECORD":
                    row_descriptions.append(f"{headers[i]}: {cell.text}")
            if row_descriptions:
                legal_descriptions.append(", ".join(row_descriptions))
        legal_description = "\n".join(legal_descriptions)
        record_value(abstract, 'legal', legal_description)
    else:
        input("No legal description found. Please review and press enter to continue.")


def record_document_fields(browser, abstract, document):
    """
    Record the document fields from the web page.

    Args:
        browser (WebDriver): The WebDriver instance.
        abstract (Abstract): The abstract information.
        document (Document): The document information.
    """
    record_indexing_information(browser, abstract, document)
    record_document_type(browser, abstract, document)
    record_parties(browser, abstract, document)
    record_related_documents(browser, abstract, document)
    record_legal(browser, abstract, document)
    record_empty_values(abstract, ['volume', 'document link', 'effective date'])
    record_comments(abstract, document)


def record(browser, abstract, document):
    """
    Record the document information if not in review mode.

    Args:
        browser (WebDriver): The WebDriver instance.
        abstract (Abstract): The abstract information.
        document (Document): The document information.
    """
    wait_for_page_to_load(browser, abstract, document)
    if not abstract.review:
        click_show_elements(browser, abstract, document)
        short_nap()
        record_document_fields(browser, abstract, document)
