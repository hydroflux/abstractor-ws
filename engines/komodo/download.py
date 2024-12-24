from selenium.webdriver.remote.webdriver import WebDriver  # Used to interact with the browser
from typing import Optional # Used to define the return type of the function
from selenium_utilities.inputs import click_button
from selenium_utilities.locators import locate_element_by_class_name, locate_element_by_css_selector, locate_element_by_tag_name

def create_document_download_value(browser: WebDriver, abstract: Abstract) -> Optional[str]:
    try:
        # Locate the Document ID element
        image_section = locate_element_by_class_name(browser, abstract.county.classes["Document Image Section"], "svg element")
        image_element = locate_element_by_tag_name(image_section, abstract.county.tags["Document Image"], "svg element")
        image_url = image_element.get_attribute(abstract.county.tags["Document Image Attribute"])
        document_id = image_url.split('/')[-1].split('_')[0]

        # Locate the Order ID element
        order_id_element = locate_element_by_css_selector(browser, abstract.county.tags["Order ID"], "order ID element")
        order_id = order_id_element.text
        
        # Create the final string
        download_value_final_string = f"{order_id}_{document_id}{abstract.county.inputs["Stock Download Suffix"]}"
        print(f"Created string: {download_value_final_string}")

        return download_value_final_string
    except Exception as e:
        print(f"An error occurred while creating the string: {e}")
        return None


def execute_download(browser, abstract, document):
    click_button(browser, locate_element_by_css_selector, abstract.county.buttons["Purchase Window"], "purchase window", document)
    click_button(browser, locate_element_by_css_selector, abstract.county.buttons["Purchase"], "purchase button", document)
    click_button(browser, locate_element_by_css_selector, abstract.county.buttons["Download"], "download button", document)
    document.download_value = create_document_download_value(browser, abstract, document)