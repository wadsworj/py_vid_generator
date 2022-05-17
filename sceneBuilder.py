from elements.elementBuilder import ElementBuilder
from elements.textElement import TextElement
from scene import Scene


class SceneBuilder:
    def __init__(self, element_builder):
        self.element_builder = element_builder

    def build(self, data):
        scene = Scene()
        scene.scene_name = data["scene_name"]
        scene.scene_index = data["scene_index"]
        scene.duration = data["duration"]

        for data_element in data["elements"]:
            element = self.element_builder.build(data_element)
            scene.add_element(element)

        return scene
