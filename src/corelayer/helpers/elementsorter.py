# Declare function to return the sorted data based on name
def sort_element_by_key(element):
    if 'layer_priority' in element:
        return element['layer_priority']
    if 'start_time' in element:
        return element['start_time'] * 100
    elif 'key_frames' in element:
        return element['key_frames'][0]['second'] * 100
    return None

# Declare function to return the sorted data based on name
def sort_by_key_elements(element):
    if hasattr(element, 'data'):
        if 'layer_priority' in element.data:
            return element.data['layer_priority']
        if 'start_time' in element.data:
            return element.data['start_time'] * 100
        elif 'key_frames' in element.data:
            return element.data['key_frames'][0]['second'] * 100
    return None


class SortByKey:
    def __init__(self, key):
        self.key = key

    # Declare function to return the sorted data based on name
    def sort_by_key(self, element):
        if self.key in element:
            return element[self.key]
        return None