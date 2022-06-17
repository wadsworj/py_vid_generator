

class ElementsViewPresenter:
    def __init__(self):
        self.data = None
        self.view = None

    def set_scene(self, scene_index):
        elements = self.build_elements_list(scene_index)
        self.view.set_elements(elements)

    def build_elements_list(self, scene_index):
        if not scene_index or not self.data:
            return

        # why isn't this zero based?
        scene_index = scene_index - 1

        elements = []
        count = 0
        scene = self.data['scenes'][scene_index]
        for element in scene['elements']:
            text = str(count)
            if 'name' in element:
                text = text + ': ' + element['name']

            if 'text' in element:
                text = text + ': ' + element['text']

            if 'type' in element:
                text = text + ': ' + element['type']

            elements.append(text)
            count = count + 1

        return elements

