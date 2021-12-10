def is_active_class(element):
    element_class = element.get_attribute("class")
    if element_class.endswith("active"):
        return True
