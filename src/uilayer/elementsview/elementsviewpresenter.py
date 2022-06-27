import copy

from src.corelayer.helpers import elementsorter
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
        self.populate_elements()

    def populate_elements(self):
        self.elements = self.build_elements_list()
        self.view.set_elements(self.elements)

    def get_element_from_text(self, item):
        selected_element_result = [x for x in self.elements if item == x[0]]
        if not selected_element_result or len(selected_element_result) < 1:
            return None
        return selected_element_result[0]

    def handle_element_click(self, item):
        selected_element = self.get_element_from_text(item)
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

        scene['elements'] = sorted(scene['elements'], key=elementsorter.sort_element_by_key, reverse=True)

        for element in scene['elements']:
            text = str(count)
            if 'name' in element:
                text = text + ': ' + element['name']

            if 'text' in element:
                text = text + ': ' + str(element['text'])

            if 'type' in element:
                text = text + ': ' + element['type']

            elements.append((text, str(count)))
            count = count + 1

        return elements

    def duplicate_selected_element(self):
        selected_text = self.view.selected_element()

        if not selected_text:
            return

        current_scene = self.data['scenes'][self.scene_index]
        selected_element = self.get_element_from_text(selected_text)

        if not selected_element:
            return

        element_data = current_scene['elements'][int(selected_element[1])]
        current_scene['elements'].append(copy.deepcopy(element_data))
        self.populate_elements()

    def delete_selected_element(self):
        selected_text = self.view.selected_element()

        if not selected_text:
            return

        current_scene = self.data['scenes'][self.scene_index]
        selected_element = self.get_element_from_text(selected_text)
        element_data = current_scene['elements'][int(selected_element[1])]

        if selected_element:
            current_scene['elements'].remove(element_data)
        self.populate_elements()
