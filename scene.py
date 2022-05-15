class Scene:
    def __init__(self, name, scene_index):
        self.name = name
        self.elements = []
        self.scene_index = scene_index
        self.finished = False

    def add_element(self, element):
        self.elements.append(element)

    def render(self, screen):
        for element in self.elements:
            element.render(screen)
