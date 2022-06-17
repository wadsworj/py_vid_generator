from src.uilayer import customuieventtype
from src.uilayer.customuievent import CustomUIEvent


class ElementsViewPresenter:
    def __init__(self):
        self.data = None
        self.view = None
        self.scene_index = None
        self.elements = []

    def set_scene(self, scene_index):
        # why isn't this zero based?
        self.scene_index = scene_index - 1
        self.elements = self.build_elements_list()
        self.view.set_elements(self.elements)

    def handle_element_click(self, item):
        selected_element_result = [x for x in self.elements if item == x[0]]

        if not selected_element_result or len(selected_element_result) < 1:
            return

        selected_element = selected_element_result[0]
        scene = self.data['scenes'][self.scene_index]
        element = scene['elements'][int(selected_element[1])]

        if element:
            event = CustomUIEvent(customuieventtype.ELEMENT_CLICKED, element)
            self.view.bubble_events_up([event])

    def build_elements_list(self):
        if self.scene_index is None or not self.data:
            return

        elements = []
        count = 0
        scene = self.data['scenes'][self.scene_index]
        for element in scene['elements']:
            text = str(count)
            if 'name' in element:
                text = text + ': ' + element['name']

            if 'text' in element:
                text = text + ': ' + element['text']

            if 'type' in element:
                text = text + ': ' + element['type']

            elements.append((text, str(count)))
            count = count + 1

        return elements

