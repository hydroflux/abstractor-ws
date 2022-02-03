

def get_previous_result_button(browser, abstract, document):
    result_buttons = locate_element_by_class_name(browser, abstract.county.classes["Result Buttons"],
                                                  "result buttons", False, document)
    return result_buttons.find_elements_by_tag_name(abstract.county.tags["Result Button"])[0]


def previous_result(browser, abstract, document):
    previous_result_button = get_previous_result_button(browser, abstract, document)
    scroll_to_top(browser)
    previous_result_button.click()
    naptime()


def get_next_result_button(browser, abstract, document):
    result_buttons = locate_element_by_class_name(browser, abstract.county.classes["Result Buttons"],
                                                  "result buttons", False, document)
    return result_buttons.find_elements_by_tag_name(abstract.county.tags["Result Button"])[1]


def click_result_button(browser, button):
    try:
        scroll_to_top(browser)
        button.click()
        short_nap()  # Nap is necessary, consider lengthening if app breaks at this point
        return True
    except ElementClickInterceptedException:
        print("Button click intercepted while trying to view previous / next result, trying again")
        # naptime()
        # button.click()
    except StaleElementReferenceException:
        print("Stale element reference exception encountered while trying to view previous / next result, trying again")
        # naptime()
        # button.click()


def handle_click_next_result_button(browser, abstract, document, button):
    while not click_result_button(browser, button):
        naptime()
        button = get_next_result_button(browser, abstract, document)


def next_result(browser, abstract, document):
    next_result_button = get_next_result_button(browser, abstract, document)
    handle_click_next_result_button(browser, abstract, document, next_result_button)