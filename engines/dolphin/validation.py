from project_management.timers import short_nap
from selenium_utilities.locators import locate_element
from settings.invalid import no_document_image


# same as "octopus", similar to "buffalo"
def check_for_document_image(browser, abstract, document):
    short_nap()
    no_document_image_element = locate_element(browser, "id", abstract.county.ids["No Document Image"],
                                               "no document image", False, document, True)
    if no_document_image_element is not None:
        if no_document_image_element.text.strip() == abstract.county.messages["No Document Image"]:
            no_document_image(abstract, document)
        else:
            return True
    else:
        input("Encountered an unknown document image error, please review and press enter to continue...")
